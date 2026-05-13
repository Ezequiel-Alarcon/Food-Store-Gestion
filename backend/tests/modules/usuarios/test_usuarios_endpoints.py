"""
Tests de integración para el módulo de administración de usuarios.

Verifica los escenarios de la sección 3 del change users-admin:
  3.4: list_users como admin retorna 200 con lista
  3.5: list_users excluye inactivos por defecto
  3.6: get_user existente retorna 200
  3.7: get_user inexistente retorna 404
  3.8: update_user como admin actualiza campos
  3.9: update_user como gestor retorna 403
  3.10: deactivate_user como admin retorna 200
  3.11: deactivate_user como gestor retorna 403
"""
from __future__ import annotations

import base64
import json

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.modules.auth.model import Usuario


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

    def put(self, url: str, params: dict | None = None):
        headers = {"Authorization": f"Bearer {self._token}"}
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{qs}" if "?" not in url else f"{url}&{qs}"
        return self._client.put(url, headers=headers)

    def delete(self, url: str):
        headers = {"Authorization": f"Bearer {self._token}"}
        return self._client.delete(url, headers=headers)


# ── Fixture de setup ─────────────────────────────────────────────────

@pytest.fixture(name="setup")
def fixture_setup(client, session):
    """Prepara la DB con usuarios de distintos roles."""
    # Admin
    admin_data = _register_and_login(client, "admin@test.com")
    _set_role(session, admin_data["user_id"], "ADMIN")

    # Gestor de stock
    stock_data = _register_and_login(client, "stock@test.com")
    _set_role(session, stock_data["user_id"], "STOCK")

    # Cliente
    client_data = _register_and_login(client, "cliente@test.com")
    _set_role(session, client_data["user_id"], "CLIENT")

    return {
        "test_client": client,
        "session": session,
        "admin": admin_data,
        "stock": stock_data,
        "cliente": client_data,
    }


# ── 3.4: list_users como admin retorna 200 con lista ─────────────────

def test_list_users_admin_retorna_200(setup):
    """3.4: GET /usuarios/ como admin retorna 200 con lista de usuarios."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/usuarios/")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) >= 3, f"Expected at least 3 users, got {len(data)}"


# ── 3.5: list_users excluye inactivos por defecto ───────────────────

def test_list_users_excluye_inactivos(setup):
    """3.5: GET /usuarios/ excluye usuarios inactivos por defecto."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    # Obtener ID del cliente
    client_user_id = setup["cliente"]["user_id"]

    # Desactivar al cliente (soft delete)
    usuario = setup["session"].get(Usuario, client_user_id)
    usuario.activo = False
    setup["session"].add(usuario)
    setup["session"].flush()

    # Listar sin incluir inactivos
    resp = ac.get("/api/v1/usuarios/", params={"include_inactive": False})

    assert resp.status_code == 200
    data = resp.json()
    user_ids = [u["id"] for u in data]
    assert client_user_id not in user_ids, f"Usuario inactivo {client_user_id} no debería estar en la lista"

    # Listar incluyendo inactivos
    resp2 = ac.get("/api/v1/usuarios/", params={"include_inactive": True})

    assert resp2.status_code == 200
    data2 = resp2.json()
    user_ids2 = [u["id"] for u in data2]
    assert client_user_id in user_ids2, f"Usuario inactivo {client_user_id} debería estar cuando include_inactive=True"


# ── 3.6: get_user existente retorna 200 ─────────────────────────────

def test_get_user_existente_retorna_200(setup):
    """3.6: GET /usuarios/{user_id} con usuario existente retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])
    admin_user_id = setup["admin"]["user_id"]

    resp = ac.get(f"/api/v1/usuarios/{admin_user_id}")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert data["id"] == admin_user_id
    assert "email" in data
    assert "nombre" in data
    assert "rol" in data


# ── 3.7: get_user inexistente retorna 404 ───────────────────────────

def test_get_user_inexistente_retorna_404(setup):
    """3.7: GET /usuarios/{user_id} con usuario inexistente retorna 404."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])

    resp = ac.get("/api/v1/usuarios/99999")

    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}: {resp.json()}"


# ── 3.8: update_user como admin actualiza campos ────────────────────

def test_update_user_admin_actualiza_campos(setup):
    """3.8: PUT /usuarios/{user_id} como admin actualiza los campos del usuario."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])
    gestor_user_id = setup["stock"]["user_id"]

    resp = ac.put(
        f"/api/v1/usuarios/{gestor_user_id}",
        params={"nombre": "Gestor Actualizado", "rol": "ADMIN"},
    )

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert data["nombre"] == "Gestor Actualizado"
    assert data["rol"] == "ADMIN"


# ── 3.9: update_user como stock retorna 403 ─────────────────────────

def test_update_user_stock_retorna_403(setup):
    """3.9: PUT /usuarios/{user_id} como stock retorna 403 Forbidden."""
    ac = AuthClient(setup["test_client"], setup["stock"]["access_token"])
    admin_user_id = setup["admin"]["user_id"]

    resp = ac.put(
        f"/api/v1/usuarios/{admin_user_id}",
        params={"nombre": "Intento de Gestor"},
    )

    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}: {resp.json()}"


# ── 3.10: deactivate_user como admin retorna 200 ───────────────────

def test_deactivate_user_admin_retorna_200(setup):
    """3.10: DELETE /usuarios/{user_id} como admin retorna 200."""
    ac = AuthClient(setup["test_client"], setup["admin"]["access_token"])
    client_user_id = setup["cliente"]["user_id"]

    resp = ac.delete(f"/api/v1/usuarios/{client_user_id}")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.json()}"
    data = resp.json()
    assert "message" in data or "Usuario desactivado" in str(data)


# ── 3.11: deactivate_user como stock retorna 403 ───────────────────

def test_deactivate_user_stock_retorna_403(setup):
    """3.11: DELETE /usuarios/{user_id} como stock retorna 403 Forbidden."""
    ac = AuthClient(setup["test_client"], setup["stock"]["access_token"])
    admin_user_id = setup["admin"]["user_id"]

    resp = ac.delete(f"/api/v1/usuarios/{admin_user_id}")

    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}: {resp.json()}"