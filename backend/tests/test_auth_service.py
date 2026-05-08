"""
Tests unitarios para AuthService.

Usa SQLite en memoria para simular la base de datos.
"""
from __future__ import annotations

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.core.security import hash_password, verify_password
from app.modules.auth.model import Usuario
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.auth.service import AuthService
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


@pytest.fixture(name="service")
def fixture_service(session):
    """AuthService con dependencias mock."""
    return AuthService(session)


class TestAuthServiceRegister:
    """Tests de registro de usuario."""

    def test_register_creates_user(self, service, session):
        """Registrar usuario debe crearlo en la DB."""
        request = RegisterRequest(
            email="test@example.com",
            password="Password1",
            nombre="Test User",
        )
        response = service.register(request)

        assert response.access_token is not None
        assert response.refresh_token is not None
        assert response.token_type == "bearer"

        # Verificar que el usuario se creó
        repo = AuthRepository(session)
        user = repo.get_user_by_email("test@example.com")
        assert user is not None
        assert user.nombre == "Test User"
        assert user.rol == "CLIENT"

    def test_register_duplicate_email(self, service):
        """Registro con email duplicado debe fallar."""
        request = RegisterRequest(
            email="dup@example.com",
            password="Password1",
            nombre="First User",
        )
        service.register(request)

        with pytest.raises(Exception) as exc:
            service.register(request)
        assert "ya está registrado" in str(exc.value.detail)

    def test_register_password_is_hashed(self, service, session):
        """Password debe almacenarse hasheado."""
        request = RegisterRequest(
            email="hash@example.com",
            password="MySecret1",
            nombre="Hash User",
        )
        service.register(request)

        repo = AuthRepository(session)
        user = repo.get_user_by_email("hash@example.com")
        assert user.password_hash != "MySecret1"
        assert verify_password("MySecret1", user.password_hash)


class TestAuthServiceLogin:
    """Tests de login."""

    def test_login_success(self, service):
        """Login con credenciales correctas debe devolver tokens."""
        # Registrar usuario primero
        request = RegisterRequest(
            email="login@example.com",
            password="Password1",
            nombre="Login User",
        )
        service.register(request)

        # Login
        login_req = LoginRequest(email="login@example.com", password="Password1")
        response = service.login(login_req)

        assert response.access_token is not None
        assert response.refresh_token is not None

    def test_login_wrong_password(self, service):
        """Login con password incorrecto debe fallar."""
        request = RegisterRequest(
            email="wrong@example.com",
            password="Password1",
            nombre="Wrong Pass",
        )
        service.register(request)

        login_req = LoginRequest(email="wrong@example.com", password="WrongPassword")
        with pytest.raises(Exception) as exc:
            service.login(login_req)
        assert "Credenciales inválidas" in str(exc.value.detail)

    def test_login_nonexistent_user(self, service):
        """Login con email no registrado debe fallar."""
        login_req = LoginRequest(email="no@example.com", password="Anything")
        with pytest.raises(Exception) as exc:
            service.login(login_req)
        assert "Credenciales inválidas" in str(exc.value.detail)


class TestAuthServiceRefresh:
    """Tests de refresh token."""

    def test_refresh_invalid_token(self, service):
        """Refresh con token inválido debe fallar."""
        from app.modules.auth.schemas import RefreshRequest

        req = RefreshRequest(refresh_token="invalid-token")
        with pytest.raises(Exception) as exc:
            service.refresh_token(req)
        assert "inválido" in str(exc.value.detail).lower()


class TestAuthServiceLogout:
    """Tests de logout."""

    def test_logout_invalid_token_no_error(self, service):
        """Logout con token inválido no debe lanzar error."""
        # No debería lanzar excepción
        service.logout("invalid-token")


class TestPasswordHashing:
    """Tests de hashing de contraseñas."""

    def test_hash_and_verify(self):
        """Verificar que hash + verify funciona."""
        hashed = hash_password("MyPassword1")
        assert hashed != "MyPassword1"
        assert verify_password("MyPassword1", hashed)

    def test_verify_wrong_password(self):
        """Verificar que password incorrecto falla."""
        hashed = hash_password("RightPassword1")
        assert not verify_password("WrongPassword1", hashed)
