"""
Fixtures compartidas para tests de integración.

Overridea get_session y SessionLocal para usar SQLite en memoria,
de modo que todos los módulos (incluyendo los que crean sesiones
manualmente via UoW) usen la misma DB de pruebas.
"""
from __future__ import annotations

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlmodel import Session, SQLModel

# ═══ MUST be set BEFORE any app import — database.py runs create_engine at import time ═══
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["RATE_LIMIT_AUTH"] = "999999"  # Deshabilitar rate limiting en tests (slowapi)

# ═══ Patch sqlmodel.create_engine to strip PostgreSQL-only kwargs for SQLite ═══
import sqlmodel as _sqlmodel_mod

_original_sqlmodel_create_engine = _sqlmodel_mod.create_engine

def _patched_create_engine(url, **kwargs):
    url_str = str(url)
    if "sqlite" in url_str:
        kwargs.pop("pool_size", None)
        kwargs.pop("max_overflow", None)
        kwargs.pop("pool_pre_ping", None)
        # StaticPool: reuse the SAME connection so all sessions share the same in-memory DB
        from sqlalchemy.pool import StaticPool
        kwargs["poolclass"] = StaticPool
        # Allow cross-thread access (FastAPI threadpool for sync endpoints)
        connect_args = kwargs.get("connect_args", {})
        connect_args["check_same_thread"] = False
        kwargs["connect_args"] = connect_args
    return _original_sqlmodel_create_engine(url, **kwargs)

_sqlmodel_mod.create_engine = _patched_create_engine

# ═══ Registrar type compiler para ARRAY → JSON en SQLite ═══
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import JSON

@compiles(ARRAY, "sqlite")
def _compile_array_sqlite(element, compiler, **kw):
    return compiler.visit_JSON(JSON(), **kw)

# Monkey-patch ARRAY.bind_processor para convertir listas Python a JSON en SQLite
import json as _json

_original_bind_processor = ARRAY.bind_processor
_original_result_processor = ARRAY.result_processor

def _patched_bind_processor(self, dialect):
    if dialect.name == "sqlite":
        def process(value):
            if value is None:
                return None
            if isinstance(value, list):
                return _json.dumps(value)
            return value
        return process
    return _original_bind_processor(self, dialect)

def _patched_result_processor(self, dialect, coltype):
    if dialect.name == "sqlite":
        def process(value):
            if value is None:
                return None
            if isinstance(value, str):
                try:
                    return _json.loads(value)
                except (_json.JSONDecodeError, TypeError):
                    return value
            return value
        return process
    return _original_result_processor(self, dialect, coltype)

ARRAY.bind_processor = _patched_bind_processor
ARRAY.result_processor = _patched_result_processor

# ── Importar TODOS los modelos para que SQLModel.metadata los registre ──
from app.modules.auth.model import Usuario  # noqa: F401
from app.modules.categorias.model import Categoria  # noqa: F401
from app.modules.direcciones.model import UserAddress, BranchAddress  # noqa: F401
from app.modules.ingredientes.model import Ingrediente  # noqa: F401
from app.modules.pedidos.model import (  # noqa: F401
    EstadoPedido,
    Pedido,
    DetallePedido,
    HistorialEstadoPedido,
)
from app.modules.productos.model import Producto, ProductoCategoria, ProductoIngrediente  # noqa: F401
from app.modules.refreshtokens.model import RefreshToken  # noqa: F401
from app.modules.sucursales.model import Sucursal  # noqa: F401

from app.main import app


@pytest.fixture(name="engine")
def fixture_engine():
    """Engine SQLite en memoria compartido con database.py."""
    # Usar el engine que database.py ya creó (única instancia en memoria)
    from app.core.database import engine as db_engine

    # Habilitar foreign keys en SQLite
    @event.listens_for(db_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Crear todas las tablas en esta única base de datos
    SQLModel.metadata.create_all(db_engine)
    return db_engine


@pytest.fixture(name="session")
def fixture_session(engine) -> Generator[Session, None, None]:
    """Sesión de prueba."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(engine):
    """TestClient de FastAPI con SessionLocal overrrideado a SQLite."""
    from app.core.database import get_session
    from sqlalchemy.orm import sessionmaker

    def override_get_session():
        session = Session(engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session

    TestSessionLocal = sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    # Override SessionLocal en database.py
    import app.core.database as db_module
    original_db_local = db_module.SessionLocal
    db_module.SessionLocal = TestSessionLocal

    # Pedidos service importa SessionLocal directamente
    import app.modules.pedidos.service as pedidos_svc
    original_pedidos_local = pedidos_svc.SessionLocal
    pedidos_svc.SessionLocal = TestSessionLocal

    # Direcciones service importa SessionLocal directamente
    import app.modules.direcciones.service as direcciones_svc
    original_direcciones_local = direcciones_svc.SessionLocal
    direcciones_svc.SessionLocal = TestSessionLocal

    with TestClient(app) as client:
        yield client

    # Restaurar valores originales
    db_module.SessionLocal = original_db_local
    pedidos_svc.SessionLocal = original_pedidos_local
    direcciones_svc.SessionLocal = original_direcciones_local
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _clean_db(engine):
    """Limpia todas las tablas entre tests para aislamiento total."""
    yield
    # Truncar todas las tablas en orden inverso de dependencias
    from sqlmodel import SQLModel
    for table in reversed(SQLModel.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())
            conn.commit()
