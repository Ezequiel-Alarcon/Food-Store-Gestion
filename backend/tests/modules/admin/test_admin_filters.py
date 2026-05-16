"""Tests de integración para endpoints admin con filtros de fecha.

Verifica:
  - GET /admin/metrics/ acepta query params desde/hasta
  - GET /admin/metrics/sales-chart/ acepta query params desde/hasta
  - GET /admin/metrics/top-products/ acepta query params desde/hasta
  - GET /admin/metrics/orders-by-status/ acepta query params desde/hasta
  - GET /admin/pedidos/{id}/ retorna schema tipado
  - GET /admin/pedidos/{id}/historial/ retorna schema tipado
"""
from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.modules.auth.model import Usuario
from app.modules.pedidos.model import DetallePedido, Pedido, EstadoPedido
from app.modules.productos.model import Producto


# ── Helpers ──────────────────────────────────────────────────────────

def _decode_jwt_sub(token: str) -> int:
    """Extrae el user_id (sub) de un JWT sin verificarlo contra DB."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token inválido")
    payload_b64 = parts[1]
    payload_b64 += "=" * (4 - len(payload_b64) % 4)
    payload_bytes = base64.urlsafe_b64decode(payload_b64)
    payload = json.loads(payload_bytes)
    return int(payload["sub"])


def _register_and_login(client: TestClient, email: str, password: str = "Password1", nombre: str = "Test", apellido: str = "Test") -> dict:
    """Registra un usuario y devuelve tokens + user_id."""
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "nombre": nombre, "apellido": apellido},
    )
    assert resp.status_code == 201, f"Register failed: {resp.json()}"
    tokens = resp.json()
    user_id = _decode_jwt_sub(tokens["access_token"])
    return {
        "user_id": user_id,
        "email": email,
        "access_token": tokens["access_token"],
    }


def _set_role(session: Session, user_id: int, rol: str) -> None:
    """Actualiza el rol de un usuario directamente en DB."""
    user = session.get(Usuario, user_id)
    user.rol = rol
    session.add(user)
    session.flush()


class AuthClient:
    """Wraps TestClient con token JWT para requests autenticados."""

    def __init__(self, client: TestClient, access_token: str):
        self._client = client
        self._token = access_token

    def get(self, url: str, params: dict | None = None):
        headers = {"Authorization": f"Bearer {self._token}"}
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{qs}" if "?" not in url else f"{url}&{qs}"
        return self._client.get(url, headers=headers)


# ── Fixture de setup ─────────────────────────────────────────────────

@pytest.fixture(name="setup")
def fixture_setup(client, session):
    """Prepara la DB con admin y datos de prueba."""
    admin_data = _register_and_login(client, "admin-filters@test.com")
    _set_role(session, admin_data["user_id"], "ADMIN")

    # Estados
    for codigo, nombre, orden, es_terminal in [
        ("PENDIENTE", "Pendiente", 1, False),
        ("CONFIRMADO", "Confirmado", 5, True),
        ("ENTREGADO", "Entregado", 6, True),
    ]:
        existing = session.get(EstadoPedido, codigo)
        if not existing:
            session.add(EstadoPedido(codigo=codigo, nombre=nombre, orden=orden, es_terminal=es_terminal))
    session.flush()

    return {
        "test_client": client,
        "session": session,
        "admin": admin_data,
    }


# ── GET /admin/metrics/ con filtros ──────────────────────────────────

def test_metrics_acepta_desde_hasta(setup):
    """GET /admin/metrics/ acepta query params desde y hasta."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/", params={
        "desde": "2025-01-01T00:00:00Z",
        "hasta": "2025-12-31T23:59:59Z",
    })

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "total_pedidos" in data
    assert "total_usuarios" in data


def test_metrics_sin_filtros(setup):
    """GET /admin/metrics/ sin filtros retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/")

    assert resp.status_code == 200
    data = resp.json()
    assert "total_pedidos" in data
    assert "total_revenue" in data
    assert "ticket_promedio" in data
    assert "total_clientes" in data
    assert "total_usuarios" in data


# ── GET /admin/metrics/sales-chart/ con filtros ──────────────────────

def test_sales_chart_acepta_desde_hasta(setup):
    """GET /admin/metrics/sales-chart/ acepta query params desde y hasta."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/sales-chart/", params={
        "desde": "2025-01-01T00:00:00Z",
        "hasta": "2025-06-30T23:59:59Z",
    })

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "datos" in data
    assert "dias" in data


def test_sales_chart_sin_filtros(setup):
    """GET /admin/metrics/sales-chart/ sin filtros usa 30 días default."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/sales-chart/")

    assert resp.status_code == 200
    data = resp.json()
    assert data["dias"] == 30


# ── GET /admin/metrics/top-products/ con filtros ─────────────────────

def test_top_products_acepta_desde_hasta(setup):
    """GET /admin/metrics/top-products/ acepta query params desde y hasta."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/top-products/", params={
        "desde": "2025-01-01T00:00:00Z",
        "hasta": "2025-12-31T23:59:59Z",
        "limit": "5",
    })

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    assert isinstance(resp.json(), list)


# ── GET /admin/metrics/orders-by-status/ con filtros ─────────────────

def test_orders_by_status_acepta_desde_hasta(setup):
    """GET /admin/metrics/orders-by-status/ acepta query params desde y hasta."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/orders-by-status/", params={
        "desde": "2025-01-01T00:00:00Z",
        "hasta": "2025-12-31T23:59:59Z",
    })

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    assert isinstance(resp.json(), list)


# ── GET /admin/pedidos/{id}/ ─────────────────────────────────────────

def test_pedido_detail_retorna_schema_tipado(setup, session):
    """GET /admin/pedidos/{id}/ retorna PedidoDetailResponse."""
    # Crear un pedido de prueba
    user_id = setup["admin"]["user_id"]
    pedido = Pedido(
        cliente_id=user_id,
        estado_codigo="PENDIENTE",
        direccion_calle="Test",
        direccion_numero="123",
        direccion_ciudad="Test City",
        direccion_provincia="Test Prov",
        direccion_pais="Argentina",
        total=150.0,
        costo_envio=10.0,
    )
    session.add(pedido)
    session.flush()

    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get(f"/api/v1/admin/pedidos/{pedido.id}/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "id" in data
    assert "cliente_id" in data
    assert "estado_codigo" in data
    assert "items" in data
    assert "direccion_calle" in data
    assert "total" in data
    assert "creado_en" in data


def test_pedido_detail_no_existe(setup):
    """GET /admin/pedidos/{id}/ para pedido inexistente retorna 404."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/pedidos/99999/")

    assert resp.status_code == 404


# ── GET /admin/pedidos/{id}/historial/ ───────────────────────────────

def test_pedido_historial_retorna_schema_tipado(setup, session):
    """GET /admin/pedidos/{id}/historial/ retorna list[PedidoHistorialEntry]."""
    user_id = setup["admin"]["user_id"]
    pedido = Pedido(
        cliente_id=user_id,
        estado_codigo="PENDIENTE",
        direccion_calle="Test",
        direccion_numero="123",
        direccion_ciudad="Test City",
        direccion_provincia="Test Prov",
        direccion_pais="Argentina",
        total=100.0,
    )
    session.add(pedido)
    session.flush()

    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get(f"/api/v1/admin/pedidos/{pedido.id}/historial/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert isinstance(data, list)


def test_pedido_historial_no_existe(setup):
    """GET /admin/pedidos/{id}/historial/ para pedido inexistente retorna 404."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/pedidos/99999/historial/")

    assert resp.status_code == 404
