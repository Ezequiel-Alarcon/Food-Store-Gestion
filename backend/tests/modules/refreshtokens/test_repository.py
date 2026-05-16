"""
Tests unitarios para RefreshTokenRepository.

Usa SQLite en memoria para simular la base de datos.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.modules.refreshtokens.model import RefreshToken
from app.modules.refreshtokens.repository import RefreshTokenRepository


@pytest.fixture(name="engine")
def fixture_engine():
    """Engine SQLite en memoria."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine):
    """Sesión de prueba."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="repo")
def fixture_repo(session):
    """RefreshTokenRepository con sesión de prueba."""
    return RefreshTokenRepository(session)


class TestRefreshTokenRepositoryCreate:
    """Tests para create."""

    def test_create_token(self, repo, session):
        """Crear un token debe almacenarlo correctamente."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token = repo.create(
            user_id=1,
            token="test-jwt-token",
            expires_at=expires_at,
        )

        assert token.id is not None
        assert token.user_id == 1
        assert token.token == "test-jwt-token"
        assert token.revocado is False
        assert token.expires_at == expires_at

    def test_create_multiple_tokens(self, repo):
        """Crear múltiples tokens para el mismo usuario."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        t1 = repo.create(user_id=1, token="token-1", expires_at=expires_at)
        t2 = repo.create(user_id=1, token="token-2", expires_at=expires_at)

        assert t1.id != t2.id
        assert t1.user_id == t2.user_id


class TestRefreshTokenRepositoryGetByToken:
    """Tests para get_by_token."""

    def test_get_existing_token(self, repo):
        """Buscar un token existente debe retornarlo."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        repo.create(user_id=1, token="find-me", expires_at=expires_at)

        result = repo.get_by_token("find-me")
        assert result is not None
        assert result.token == "find-me"
        assert result.user_id == 1

    def test_get_nonexistent_token(self, repo):
        """Buscar un token inexistente debe retornar None."""
        result = repo.get_by_token("does-not-exist")
        assert result is None


class TestRefreshTokenRepositoryGetValidToken:
    """Tests para get_valid_token."""

    def test_get_valid_token(self, repo):
        """Buscar un token válido debe retornarlo."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        repo.create(user_id=1, token="valid-token", expires_at=expires_at)

        result = repo.get_valid_token("valid-token")
        assert result is not None
        assert result.token == "valid-token"
        assert result.revocado is False

    def test_get_revoked_token(self, repo):
        """Buscar un token revocado debe retornar None."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token = repo.create(user_id=1, token="revoked-token", expires_at=expires_at)
        repo.revoke(token)

        result = repo.get_valid_token("revoked-token")
        assert result is None

    def test_get_expired_token(self, repo):
        """Buscar un token expirado debe retornar None."""
        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        repo.create(user_id=1, token="expired-token", expires_at=expires_at)

        result = repo.get_valid_token("expired-token")
        assert result is None


class TestRefreshTokenRepositoryRevoke:
    """Tests para revoke."""

    def test_revoke_token(self, repo):
        """Revocar un token debe marcarlo como revocado."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token = repo.create(user_id=1, token="to-revoke", expires_at=expires_at)

        assert token.revocado is False
        repo.revoke(token)
        assert token.revocado is True

    def test_revoke_already_revoked(self, repo):
        """Revocar un token ya revocado no debe fallar."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token = repo.create(user_id=1, token="double-revoke", expires_at=expires_at)
        repo.revoke(token)
        repo.revoke(token)
        assert token.revocado is True


class TestRefreshTokenRepositoryRevokeAllByUser:
    """Tests para revoke_all_by_user."""

    def test_revoke_all_tokens(self, repo):
        """Revocar todos los tokens de un usuario."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        repo.create(user_id=42, token="t1", expires_at=expires_at)
        repo.create(user_id=42, token="t2", expires_at=expires_at)
        repo.create(user_id=42, token="t3", expires_at=expires_at)

        count = repo.revoke_all_by_user(42)
        assert count == 3

    def test_revoke_all_empty(self, repo):
        """Revocar tokens de usuario sin tokens debe retornar 0."""
        count = repo.revoke_all_by_user(999)
        assert count == 0

    def test_revoke_all_excludes_already_revoked(self, repo):
        """revoke_all_by_user solo cuenta los no revocados."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        t1 = repo.create(user_id=55, token="active-1", expires_at=expires_at)
        repo.create(user_id=55, token="active-2", expires_at=expires_at)
        repo.revoke(t1)

        count = repo.revoke_all_by_user(55)
        assert count == 1


class TestRefreshTokenRepositoryGetActiveTokensByUser:
    """Tests para get_active_tokens_by_user."""

    def test_get_active_tokens(self, repo):
        """Obtener tokens activos de un usuario."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        repo.create(user_id=10, token="active-1", expires_at=expires_at)
        repo.create(user_id=10, token="active-2", expires_at=expires_at)

        tokens = repo.get_active_tokens_by_user(10)
        assert len(tokens) == 2

    def test_get_active_excludes_revoked(self, repo):
        """Tokens revocados no deben aparecer en activos."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        t1 = repo.create(user_id=20, token="will-revoke", expires_at=expires_at)
        repo.create(user_id=20, token="stays-active", expires_at=expires_at)
        repo.revoke(t1)

        tokens = repo.get_active_tokens_by_user(20)
        assert len(tokens) == 1
        assert tokens[0].token == "stays-active"

    def test_get_active_excludes_expired(self, repo):
        """Tokens expirados no deben aparecer en activos."""
        future = datetime.now(timezone.utc) + timedelta(days=7)
        past = datetime.now(timezone.utc) - timedelta(days=1)
        repo.create(user_id=30, token="expired", expires_at=past)
        repo.create(user_id=30, token="valid", expires_at=future)

        tokens = repo.get_active_tokens_by_user(30)
        assert len(tokens) == 1
        assert tokens[0].token == "valid"

    def test_get_active_no_tokens(self, repo):
        """Usuario sin tokens debe retornar lista vacía."""
        tokens = repo.get_active_tokens_by_user(999)
        assert tokens == []
