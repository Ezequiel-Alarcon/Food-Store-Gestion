"""
Tests de integración para endpoints de perfil.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


class TestPerfilEndpoints:
    """Tests de integración para /api/v1/perfil."""

    def _register_and_login(self, client: TestClient) -> str:
        """Helper: registra y hace login, retorna access_token."""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "perfil@example.com",
                "password": "Password1",
                "nombre": "Perfil User",
            },
        )

        login_resp = client.post(
            "/api/v1/auth/login",
            json={"email": "perfil@example.com", "password": "Password1"},
        )
        return login_resp.json()["access_token"]

    def test_get_perfil_authenticated(self, client: TestClient):
        """GET /perfil autenticado debe devolver datos."""
        token = self._register_and_login(client)

        response = client.get(
            "/api/v1/perfil",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "perfil@example.com"
        assert data["nombre"] == "Perfil User"
        assert data["rol"] == "CLIENT"

    def test_get_perfil_unauthenticated(self, client: TestClient):
        """GET /perfil sin token debe devolver 401."""
        response = client.get("/api/v1/perfil")
        assert response.status_code == 401

    def test_update_perfil(self, client: TestClient):
        """PUT /perfil debe actualizar nombre y teléfono."""
        token = self._register_and_login(client)

        response = client.put(
            "/api/v1/perfil",
            json={"nombre": "Updated Name", "telefono": "+5491123456789"},
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Updated Name"
        assert data["telefono"] == "+5491123456789"

    def test_change_password(self, client: TestClient):
        """PUT /perfil/password debe cambiar la contraseña."""
        token = self._register_and_login(client)

        response = client.put(
            "/api/v1/perfil/password",
            json={
                "current_password": "Password1",
                "new_password": "NewPass1",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "actualizada" in response.json()["message"]

    def test_change_password_wrong_current(self, client: TestClient):
        """Cambiar password con current erróneo debe fallar."""
        token = self._register_and_login(client)

        response = client.put(
            "/api/v1/perfil/password",
            json={
                "current_password": "WrongPassword",
                "new_password": "NewPass1",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
