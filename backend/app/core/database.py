"""
Configuración de base de datos con SQLModel.
Proveé engine y session factory para PostgreSQL.
"""
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

# Engine con pool de conexiones
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory para UoW pattern
SessionLocal = Session(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Generator[Session, None, None]:
    """
    Generador de sesión para inyección de dependencias.
    Uso: Depends(get_session)
    """
    with SessionLocal as session:
        yield session


def init_db() -> None:
    """Inicializa la base de datos creando todas las tablas."""
    SQLModel.metadata.create_all(engine)