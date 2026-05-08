"""
app.modules.refreshtokens.service

Servicio para gestión de refresh tokens.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlmodel import Session

from app.core.config import get_settings
from app.modules.refreshtokens.model import RefreshToken
from app.modules.refreshtokens.repository import RefreshTokenRepository

settings = get_settings()


class RefreshTokenService:
    """
    Servicio de refresh tokens.
    
    Opera con RefreshTokenRepository.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.repo = RefreshTokenRepository(session)
    
    def create(self, user_id: int, token: str) -> RefreshToken:
        """Crea un nuevo refresh token."""
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        return self.repo.create(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
    
    def get_valid(self, token: str) -> RefreshToken | None:
        """Busca un token válido."""
        return self.repo.get_valid_token(token)
    
    def revoke(self, token: RefreshToken) -> None:
        """Revoca un token."""
        self.repo.revoke(token)
    
    def revoke_all_by_user(self, user_id: int) -> int:
        """Revoca todos los tokens de un usuario."""
        return self.repo.revoke_all_by_user(user_id)
