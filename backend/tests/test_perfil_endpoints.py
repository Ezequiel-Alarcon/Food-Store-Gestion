"""
Tests de integración para endpoints de perfil.
"""
from __future__ import annotations

from fastapi.testclient import TestClient
from sqlmodel import Session


class TestPerfilEndpoints:
    """Tests de integración para /api/v1/perfil."""

    def _register_and_login(self, session: Session) -> str:
        """Helper: crea usuario directo en BD y retorna access_token JWT."""
        from app.core.security import create_access_token, hash_password
        from app.modules.auth.model import Usuario

        user = Usuario(
            email="perfil@example.com",
            nombre="Perfil User",
            apellido="Test",
            password_hash=hash_password("Password1"),
            rol="CLIENT",
            activo=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        token = create_access_token(data={"sub": str(user.id), "rol": user.rol})
        return token

    def test_get_perfil_authenticated(self, client: TestClient, session: Session):
        """GET /perfil autenticado debe devolver datos."""
        token = self._register_and_login(session)

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
        """GET /perfil sin token debe devolver 401 (HTTPBearer returns 401 for missing credentials)."""
        response = client.get("/api/v1/perfil")
        assert response.status_code == 401

    def test_update_perfil(self, client: TestClient, session: Session):
        """PUT /perfil debe actualizar nombre y teléfono."""
        token = self._register_and_login(session)

        response = client.put(
            "/api/v1/perfil",
            json={"nombre": "Updated Name", "telefono": "+5491123456789"},
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Updated Name"
        assert data["telefono"] == "+5491123456789"

    def test_change_password(self, client: TestClient, session: Session):
        """PUT /perfil/password debe cambiar la contraseña."""
        token = self._register_and_login(session)

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

    def test_change_password_wrong_current(self, client: TestClient, session: Session):
        """Cambiar password con current erróneo debe fallar."""
        token = self._register_and_login(session)

        response = client.put(
            "/api/v1/perfil/password",
            json={
                "current_password": "WrongPassword",
                "new_password": "NewPass1",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401
