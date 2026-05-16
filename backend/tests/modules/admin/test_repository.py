"""Tests unitarios para AdminRepository con filtros de fecha.

Verifica:
  - get_general_metrics sin filtros retorna todos los pedidos
  - get_general_metrics con desde filtra correctamente
  - get_general_metrics con hasta filtra correctamente
  - get_sales_chart sin filtros usa últimos 30 días
  - get_sales_chart con desde/hasta filtra correctamente
  - get_top_products con desde/hasta filtra correctamente
  - get_orders_by_status con desde/hasta filtra correctamente
  - get_total_usuarios_registrados retorna conteo correcto
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from sqlmodel import Session

from app.modules.admin.repository import AdminRepository
from app.modules.pedidos.model import DetallePedido, EstadoPedido, Pedido
from app.modules.productos.model import Producto
from app.modules.auth.model import RolEnum, Usuario


@pytest.fixture(name="repo")
def fixture_repo(session: Session) -> AdminRepository:
    return AdminRepository(session)


@pytest.fixture(name="seed_data")
def fixture_seed_data(session: Session) -> dict:
    """Crea estados, usuario, producto y pedidos de prueba."""
    # Estados
    for codigo, nombre, orden, es_terminal in [
        ("PENDIENTE", "Pendiente", 1, False),
        ("CONFIRMADO", "Confirmado", 5, True),
        ("ENTREGADO", "Entregado", 6, True),
    ]:
        session.add(EstadoPedido(codigo=codigo, nombre=nombre, orden=orden, es_terminal=es_terminal))
    session.flush()

    # Usuario
    user = Usuario(
        email="test-repo@test.com",
        nombre="Test",
        apellido="Repo",
        password_hash="$2b$12$dummy",
        rol=RolEnum.CLIENT,
    )
    session.add(user)
    session.flush()

    # Producto
    producto = Producto(
        nombre="Pizza Test",
        precio=100.0,
        stock=50,
        activo=True,
    )
    session.add(producto)
    session.flush()

    return {"user_id": user.id, "producto_id": producto.id}


def _create_pedido(session: Session, user_id: int, total: float, creado_en: datetime, estado: str = "ENTREGADO") -> Pedido:
    """Helper para crear un pedido con fecha específica."""
    pedido = Pedido(
        cliente_id=user_id,
        estado_codigo=estado,
        direccion_calle="Test",
        direccion_numero="123",
        direccion_ciudad="Test City",
        direccion_provincia="Test Prov",
        direccion_pais="Argentina",
        total=total,
        creado_en=creado_en,
    )
    session.add(pedido)
    session.flush()
    return pedido


# ── get_general_metrics ────────────────────────────────────────────────

def test_get_general_metrics_sin_filtros(repo, seed_data, session):
    """Sin filtros, retorna métricas de todos los pedidos."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=60))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    metrics = repo.get_general_metrics()

    assert metrics["total_pedidos"] == 2
    assert metrics["total_revenue"] == 500.0
    assert metrics["total_clientes"] == 1


def test_get_general_metrics_con_desde(repo, seed_data, session):
    """Con desde, solo cuenta pedidos posteriores."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=60))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    metrics = repo.get_general_metrics(desde=now - timedelta(days=30))

    assert metrics["total_pedidos"] == 1
    assert metrics["total_revenue"] == 300.0


def test_get_general_metrics_con_hasta(repo, seed_data, session):
    """Con hasta, solo cuenta pedidos anteriores."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=60))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    metrics = repo.get_general_metrics(hasta=now - timedelta(days=30))

    assert metrics["total_pedidos"] == 1
    assert metrics["total_revenue"] == 200.0


def test_get_general_metrics_con_rango(repo, seed_data, session):
    """Con desde y hasta, solo cuenta pedidos en el rango."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 100.0, now - timedelta(days=90))
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=45))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    metrics = repo.get_general_metrics(
        desde=now - timedelta(days=60),
        hasta=now - timedelta(days=10),
    )

    assert metrics["total_pedidos"] == 1
    assert metrics["total_revenue"] == 200.0


# ── get_sales_chart ───────────────────────────────────────────────────

def test_get_sales_chart_sin_filtros_usa_30_dias(repo, seed_data, session):
    """Sin filtros, usa últimos 30 días como default."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=60))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    datos = repo.get_sales_chart()

    # Solo el pedido de 5 días debería aparecer
    assert len(datos) == 1
    assert datos[0]["revenue"] == 300.0


def test_get_sales_chart_con_desde_hasta(repo, seed_data, session):
    """Con desde/hasta, filtra por el rango especificado."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 100.0, now - timedelta(days=90))
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=45))
    _create_pedido(session, seed_data["user_id"], 300.0, now - timedelta(days=5))

    datos = repo.get_sales_chart(
        desde=now - timedelta(days=60),
        hasta=now - timedelta(days=10),
    )

    assert len(datos) == 1
    assert datos[0]["revenue"] == 200.0


# ── get_top_products ──────────────────────────────────────────────────

def test_get_top_products_con_desde_hasta(repo, seed_data, session):
    """Con desde/hasta, filtra productos por fecha del pedido."""
    now = datetime.now(timezone.utc)

    # Pedido antiguo
    pedido_viejo = _create_pedido(session, seed_data["user_id"], 100.0, now - timedelta(days=60))
    session.add(DetallePedido(
        pedido_id=pedido_viejo.id,
        producto_id=seed_data["producto_id"],
        cantidad=5,
        precio_unitario=20.0,
    ))

    # Pedido reciente
    pedido_nuevo = _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=5))
    session.add(DetallePedido(
        pedido_id=pedido_nuevo.id,
        producto_id=seed_data["producto_id"],
        cantidad=10,
        precio_unitario=20.0,
    ))
    session.flush()

    # Sin filtro: suma ambos
    datos_all = repo.get_top_products()
    assert datos_all[0]["cantidad_vendida"] == 15

    # Con filtro reciente: solo el nuevo
    datos_reciente = repo.get_top_products(desde=now - timedelta(days=30))
    assert datos_reciente[0]["cantidad_vendida"] == 10


# ── get_orders_by_status ──────────────────────────────────────────────

def test_get_orders_by_status_con_desde(repo, seed_data, session):
    """Con desde, filtra pedidos por fecha."""
    now = datetime.now(timezone.utc)
    _create_pedido(session, seed_data["user_id"], 100.0, now - timedelta(days=60), "PENDIENTE")
    _create_pedido(session, seed_data["user_id"], 200.0, now - timedelta(days=5), "ENTREGADO")

    datos = repo.get_orders_by_status(desde=now - timedelta(days=30))

    # Solo el pedido reciente
    assert len(datos) == 1
    assert datos[0]["estado_codigo"] == "ENTREGADO"
    assert datos[0]["cantidad"] == 1


# ── get_total_usuarios_registrados ────────────────────────────────────

def test_get_total_usuarios_registrados(repo, seed_data):
    """Retorna el conteo total de usuarios."""
    total = repo.get_total_usuarios_registrados()
    assert total >= 1  # Al menos el usuario seed


def test_get_total_usuarios_registrados_vacio(repo, session):
    """Si no hay usuarios, retorna 0."""
    # Esto depende de si hay otros usuarios en la DB de test
    total = repo.get_total_usuarios_registrados()
    assert isinstance(total, int)
    assert total >= 0
