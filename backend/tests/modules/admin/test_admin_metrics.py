"""Tests de integración para el módulo admin-metrics.

Verifica:
  - test_general_metrics_admin_retorna_200
  - test_general_metrics_gestor_retorna_200
  - test_general_metrics_client_retorna_403
  - test_sales_chart_admin_retorna_200
  - test_top_products_admin_retorna_200
  - test_orders_by_status_admin_retorna_200
"""
from __future__ import annotations

import base64
import json

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
    """Registra un usuario y devuelve tokens + user_id extraído del JWT."""
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


# ── AuthClient helper ─────────────────────────────────────────────────

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
    """Prepara la DB con usuarios de distintos roles y datos de prueba."""
    # Admin
    admin_data = _register_and_login(client, "admin-metrics@test.com")
    _set_role(session, admin_data["user_id"], "ADMIN")

    # Gestor de stock
    gestor_data = _register_and_login(client, "stock-metrics@test.com")
    _set_role(session, gestor_data["user_id"], "STOCK")

    # Cliente
    cliente_data = _register_and_login(client, "cliente-metrics@test.com")
    _set_role(session, cliente_data["user_id"], "CLIENT")

    # Seed estado ENTREGADO (necesario para las métricas)
    estado_entregado = EstadoPedido(codigo="ENTREGADO", nombre="Entregado", orden=6, es_terminal=True)
    session.add(estado_entregado)
    session.flush()

    return {
        "test_client": client,
        "session": session,
        "admin": admin_data,
        "stock": gestor_data,
        "cliente": cliente_data,
    }


# ── GET /admin/metrics/ ──────────────────────────────────────────────

def test_general_metrics_admin_retorna_200(setup):
    """GET /admin/metrics/ como admin retorna 200 con métricas."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "total_pedidos" in data
    assert "total_revenue" in data
    assert "ticket_promedio" in data
    assert "total_clientes" in data


def test_general_metrics_gestor_retorna_200(setup):
    """GET /admin/metrics/ como gestor retorna 200."""
    ac = AuthClient(setup["test_client"], setup["stock"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"


def test_general_metrics_client_retorna_403(setup):
    """GET /admin/metrics/ como cliente retorna 403 Forbidden."""
    ac = AuthClient(setup["test_client"], setup["cliente"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/")

    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}: {resp.json()}"


# ── GET /admin/metrics/sales-chart/ ──────────────────────────────────

def test_sales_chart_admin_retorna_200(setup):
    """GET /admin/metrics/sales-chart/ como admin retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/sales-chart/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "datos" in data
    assert "dias" in data
    assert isinstance(data["datos"], list)
    assert data["dias"] == 30


# ── GET /admin/metrics/top-products/ ────────────────────────────────

def test_top_products_admin_retorna_200(setup):
    """GET /admin/metrics/top-products/ como admin retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/top-products/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert isinstance(data, list)


# ── GET /admin/metrics/orders-by-status/ ─────────────────────────────

def test_orders_by_status_admin_retorna_200(setup):
    """GET /admin/metrics/orders-by-status/ como admin retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/admin/metrics/orders-by-status/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert isinstance(data, list)
    # Al menos debería tener las categorías de estado definidas
    if data:
        assert "estado_codigo" in data[0]
        assert "cantidad" in data[0]