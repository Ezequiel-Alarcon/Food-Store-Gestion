"""
Tests de integración para endpoints de refresh tokens.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import create_access_token, create_refresh_token
from app.modules.auth.model import Usuario
from app.modules.refreshtokens.model import RefreshToken


def _create_admin_token(client: TestClient, session: Session) -> str:
    """Crea un usuario admin y retorna su access token."""
    admin = Usuario(
        email="admin@test.com",
        password_hash="$2b$12$dummy",
        nombre="Admin",
        apellido="User",
        rol="ADMIN",
    )
    session.add(admin)
    session.flush()

    token_data = {
        "sub": str(admin.id),
        "email": admin.email,
        "role": admin.rol,
    }
    return create_access_token(token_data)


def _create_client_token(client: TestClient, session: Session) -> str:
    """Crea un usuario cliente y retorna su access token."""
    user = Usuario(
        email="client@test.com",
        password_hash="$2b$12$dummy",
        nombre="Client",
        apellido="User",
        rol="CLIENT",
    )
    session.add(user)
    session.flush()

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.rol,
    }
    return create_access_token(token_data)


class TestRefreshTokenEndpointsAuth:
    """Tests de autorización para endpoints de refresh tokens."""

    def test_list_tokens_no_auth(self, client: TestClient):
        """Sin token debe retornar 403."""
        response = client.get("/api/v1/refreshtokens/user/1")
        assert response.status_code in (401, 403)

    def test_list_tokens_non_admin(self, client: TestClient, session: Session):
        """Usuario no-admin debe retornar 403."""
        token = _create_client_token(client, session)
        response = client.get(
            "/api/v1/refreshtokens/user/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_revoke_token_no_auth(self, client: TestClient):
        """Sin token debe retornar 403."""
        response = client.post("/api/v1/refreshtokens/revoke/1")
        assert response.status_code in (401, 403)

    def test_revoke_token_non_admin(self, client: TestClient, session: Session):
        """Usuario no-admin debe retornar 403."""
        token = _create_client_token(client, session)
        response = client.post(
            "/api/v1/refreshtokens/revoke/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_bulk_revoke_no_auth(self, client: TestClient):
        """Sin token debe retornar 403."""
        response = client.delete("/api/v1/refreshtokens/user/1/all")
        assert response.status_code in (401, 403)

    def test_bulk_revoke_non_admin(self, client: TestClient, session: Session):
        """Usuario no-admin debe retornar 403."""
        token = _create_client_token(client, session)
        response = client.delete(
            "/api/v1/refreshtokens/user/1/all",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403


class TestListUserTokens:
    """Tests para GET /refreshtokens/user/{user_id}."""

    def test_list_empty(self, client: TestClient, session: Session):
        """Usuario sin tokens debe retornar lista vacía."""
        token = _create_admin_token(client, session)
        response = client.get(
            "/api/v1/refreshtokens/user/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["count"] == 0

    def test_list_active_tokens(self, client: TestClient, session: Session):
        """Debe retornar solo tokens activos."""
        admin_token = _create_admin_token(client, session)

        user = Usuario(
            email="target@test.com",
            password_hash="$2b$12$dummy",
            nombre="Target",
            apellido="User",
            rol="CLIENT",
        )
        session.add(user)
        session.flush()

        future = datetime.now(timezone.utc) + timedelta(days=7)
        past = datetime.now(timezone.utc) - timedelta(days=1)
        session.add(RefreshToken(user_id=user.id, token="active-t1", expires_at=future))
        session.add(RefreshToken(user_id=user.id, token="active-t2", expires_at=future))
        session.add(RefreshToken(user_id=user.id, token="expired-t", expires_at=past))
        session.commit()

        response = client.get(
            f"/api/v1/refreshtokens/user/{user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["items"]) == 2


class TestRevokeToken:
    """Tests para POST /refreshtokens/revoke/{token_id}."""

    def test_revoke_success(self, client: TestClient, session: Session):
        """Revocar token existente debe ser exitoso."""
        admin_token = _create_admin_token(client, session)

        user = Usuario(
            email="revoke-target@test.com",
            password_hash="$2b$12$dummy",
            nombre="Revoke",
            apellido="Target",
            rol="CLIENT",
        )
        session.add(user)
        session.flush()

        future = datetime.now(timezone.utc) + timedelta(days=7)
        rt = RefreshToken(user_id=user.id, token="to-revoke", expires_at=future)
        session.add(rt)
        session.commit()
        session.refresh(rt)

        response = client.post(
            f"/api/v1/refreshtokens/revoke/{rt.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == rt.id
        assert data["user_id"] == user.id
        assert "revocado" in data["message"].lower()

    def test_revoke_not_found(self, client: TestClient, session: Session):
        """Revocar token inexistente debe retornar 404."""
        admin_token = _create_admin_token(client, session)

        response = client.post(
            "/api/v1/refreshtokens/revoke/99999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    def test_revoke_already_revoked(self, client: TestClient, session: Session):
        """Revocar token ya revocado debe retornar 400."""
        admin_token = _create_admin_token(client, session)

        user = Usuario(
            email="already-revoked@test.com",
            password_hash="$2b$12$dummy",
            nombre="Already",
            apellido="Revoked",
            rol="CLIENT",
        )
        session.add(user)
        session.flush()

        future = datetime.now(timezone.utc) + timedelta(days=7)
        rt = RefreshToken(
            user_id=user.id, token="already-revoked", expires_at=future, revocado=True
        )
        session.add(rt)
        session.commit()
        session.refresh(rt)

        response = client.post(
            f"/api/v1/refreshtokens/revoke/{rt.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400


class TestBulkRevokeAll:
    """Tests para DELETE /refreshtokens/user/{user_id}/all."""

    def test_bulk_revoke_success(self, client: TestClient, session: Session):
        """Revocar todos los tokens de un usuario."""
        admin_token = _create_admin_token(client, session)

        user = Usuario(
            email="bulk-revoke@test.com",
            password_hash="$2b$12$dummy",
            nombre="Bulk",
            apellido="Revoke",
            rol="CLIENT",
        )
        session.add(user)
        session.flush()

        future = datetime.now(timezone.utc) + timedelta(days=7)
        session.add(RefreshToken(user_id=user.id, token="bulk-1", expires_at=future))
        session.add(RefreshToken(user_id=user.id, token="bulk-2", expires_at=future))
        session.add(RefreshToken(user_id=user.id, token="bulk-3", expires_at=future))
        session.commit()

        response = client.delete(
            f"/api/v1/refreshtokens/user/{user.id}/all",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user.id
        assert data["revoked_count"] == 3

    def test_bulk_revoke_no_tokens(self, client: TestClient, session: Session):
        """Revocar tokens de usuario sin tokens debe retornar 0."""
        admin_token = _create_admin_token(client, session)

        response = client.delete(
            "/api/v1/refreshtokens/user/99999/all",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["revoked_count"] == 0
