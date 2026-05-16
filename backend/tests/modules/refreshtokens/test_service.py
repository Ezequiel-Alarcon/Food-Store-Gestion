"""
Tests unitarios para RefreshTokenService con Unit of Work.

Mockea el UnitOfWork para aislar la lógica del service.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from app.modules.refreshtokens.model import RefreshToken
from app.modules.refreshtokens.service import RefreshTokenService


@pytest.fixture(name="mock_uow")
def fixture_mock_uow():
    """UnitOfWork mockeado."""
    uow = MagicMock()
    mock_session = MagicMock()
    type(uow).session = PropertyMock(return_value=mock_session)
    return uow


@pytest.fixture(name="service")
def fixture_service(mock_uow):
    """RefreshTokenService con UoW mockeado."""
    return RefreshTokenService(uow=mock_uow)


class TestRefreshTokenServiceCreate:
    """Tests para create."""

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_create_calls_uow_context(self, MockRepo, service, mock_uow):
        """create debe usar el context manager del UoW."""
        mock_token = MagicMock(spec=RefreshToken)
        MockRepo.return_value.create.return_value = mock_token

        result = service.create(user_id=1, token="jwt-token")

        assert result == mock_token
        MockRepo.assert_called_once()
        MockRepo.return_value.create.assert_called_once()

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_create_sets_expires_at(self, MockRepo, service, mock_uow):
        """create debe calcular expires_at basado en settings."""
        mock_token = MagicMock(spec=RefreshToken)
        MockRepo.return_value.create.return_value = mock_token

        service.create(user_id=1, token="jwt-token")

        call_kwargs = MockRepo.return_value.create.call_args[1]
        assert call_kwargs["user_id"] == 1
        assert call_kwargs["token"] == "jwt-token"
        assert "expires_at" in call_kwargs
        assert call_kwargs["expires_at"] > datetime.now(timezone.utc)


class TestRefreshTokenServiceGetValid:
    """Tests para get_valid."""

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_get_valid_returns_token(self, MockRepo, service):
        """get_valid debe retornar el token si es válido."""
        mock_token = MagicMock(spec=RefreshToken)
        MockRepo.return_value.get_valid_token.return_value = mock_token
        mock_session = MagicMock()

        result = service.get_valid(mock_session, "valid-jwt")

        assert result == mock_token
        MockRepo.assert_called_once_with(mock_session)
        MockRepo.return_value.get_valid_token.assert_called_once_with("valid-jwt")

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_get_valid_returns_none(self, MockRepo, service):
        """get_valid debe retornar None si el token no es válido."""
        MockRepo.return_value.get_valid_token.return_value = None
        mock_session = MagicMock()

        result = service.get_valid(mock_session, "invalid-jwt")

        assert result is None


class TestRefreshTokenServiceRevoke:
    """Tests para revoke."""

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_revokes_token(self, MockRepo, service, mock_uow):
        """revoke debe llamar al repo.revoke dentro del UoW."""
        mock_token = MagicMock(spec=RefreshToken)

        service.revoke(mock_token)

        MockRepo.return_value.revoke.assert_called_once_with(mock_token)


class TestRefreshTokenServiceRevokeAllByUser:
    """Tests para revoke_all_by_user."""

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_revokes_all_tokens(self, MockRepo, service, mock_uow):
        """revoke_all_by_user debe retornar la cantidad revocada."""
        MockRepo.return_value.revoke_all_by_user.return_value = 5

        count = service.revoke_all_by_user(user_id=42)

        assert count == 5
        MockRepo.return_value.revoke_all_by_user.assert_called_once_with(user_id=42)

    @patch("app.modules.refreshtokens.service.RefreshTokenRepository")
    def test_revokes_zero_when_no_tokens(self, MockRepo, service, mock_uow):
        """revoke_all_by_user debe retornar 0 si no hay tokens."""
        MockRepo.return_value.revoke_all_by_user.return_value = 0

        count = service.revoke_all_by_user(user_id=999)

        assert count == 0
