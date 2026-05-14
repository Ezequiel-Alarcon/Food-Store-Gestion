"""
app.modules.auth.service

Servicio de autenticación: registro, login, refresh, logout.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from app.core.exceptions import ConflictError, UnauthorizedError
from sqlmodel import Session

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.modules.auth.model import Usuario
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.modules.refreshtokens.repository import RefreshTokenRepository

settings = get_settings()


class AuthService:
    """
    Servicio de autenticación.
    
    Opera con AuthRepository y RefreshTokenRepository.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.auth_repo = AuthRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)
    
    def register(self, request: RegisterRequest) -> TokenResponse:
        """Registra un nuevo usuario y devuelve tokens."""
        # Verificar email único
        if self.auth_repo.get_user_by_email(request.email):
            raise ConflictError("El email ya está registrado")
        
        # Hashear password
        password_hash = hash_password(request.password)
        
        # Crear usuario
        usuario = self.auth_repo.create_user(
            email=request.email,
            nombre=request.nombre,
            apellido=request.apellido,
            password_hash=password_hash,
            rol="CLIENT",
            telefono=request.telefono,
        )
        
        return self._create_token_pair(usuario)
    
    def login(self, request: LoginRequest) -> TokenResponse:
        """Autentica un usuario y devuelve tokens.

        RN-AU08: Mismo mensaje para todos los casos de fallo
        (email inexistente, password incorrecto, usuario inactivo).
        """
        # Buscar usuario
        usuario = self.auth_repo.get_user_by_email(request.email)

        # Verificar credenciales: todos los fallos devuelven el mismo mensaje
        if not usuario or not verify_password(request.password, usuario.password_hash):
            raise UnauthorizedError("Credenciales inválidas")

        if not usuario.activo:
            raise UnauthorizedError("Credenciales inválidas")

        return self._create_token_pair(usuario)
    
    def refresh_token(self, request: RefreshRequest) -> TokenResponse:
        """Renueva access token usando refresh token."""
        # Decodificar el JWT para obtener user_id
        try:
            payload = decode_token(request.refresh_token)
        except ValueError:
            raise UnauthorizedError("Refresh token inválido")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Token inválido")

        stored_token = self.refresh_repo.get_valid_token(request.refresh_token)
        if not stored_token:
            raise UnauthorizedError("Refresh token expirado o revocado")

        usuario = self.auth_repo.get_by_id(stored_token.user_id)
        if not usuario:
            raise UnauthorizedError("Usuario no encontrado")

        if not usuario.activo:
            raise UnauthorizedError("Credenciales inválidas")

        # Revocar token actual y generar nuevo par (token rotation atómico)
        return self._rotate_token_pair(stored_token, usuario)
    
    def logout(self, refresh_token: str) -> None:
        """Cierra sesión revocando el refresh token."""
        stored_token = self.refresh_repo.get_by_token(refresh_token)
        if stored_token:
            self.refresh_repo.revoke(stored_token)
    
    def _create_token_pair(self, usuario: Usuario) -> TokenResponse:
        """Genera access_token + refresh_token para un usuario."""
        # Token data
        token_data = {
            "sub": str(usuario.id),
            "email": usuario.email,
            "role": usuario.rol.value if hasattr(usuario.rol, "value") else usuario.rol,
        }
        
        # Crear tokens
        access_token = create_access_token(token_data)
        refresh_token_str = create_refresh_token(token_data)
        
        # Almacenar refresh token en DB
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        self.refresh_repo.create(
            user_id=usuario.id,
            token=refresh_token_str,
            expires_at=expires_at,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def _rotate_token_pair(self, stored_token, usuario):
        """Atomically rotate token pair with rollback on failure."""
        self.refresh_repo.revoke(stored_token)
        try:
            return self._create_token_pair(usuario)
        except Exception:
            self.session.rollback()
            raise
