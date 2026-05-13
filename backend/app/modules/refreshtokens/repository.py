"""
app.modules.refreshtokens.repository

Repository para operaciones de refresh tokens.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select, update

from app.core.repository import BaseRepository
from app.modules.refreshtokens.model import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """
    Repository para operaciones de refresh tokens.
    
    Métodos:
    - create: crea un nuevo refresh token
    - get_by_token: busca un token específico
    - revoke: marca un token como revocado
    - revoke_all_by_user: invalida todos los tokens de un usuario
    """
    
    def __init__(self, session: Session):
        super().__init__(session, RefreshToken)
    
    def create(
        self,
        user_id: int,
        token: str,
        expires_at: datetime,
    ) -> RefreshToken:
        """Crea un nuevo refresh token."""
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            revocado=False,
            expires_at=expires_at,
        )
        self.session.add(refresh_token)
        self.session.flush()
        return refresh_token
    
    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Busca un refresh token por su valor."""
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        return self.session.exec(stmt).first()
    
    def get_valid_token(self, token: str) -> Optional[RefreshToken]:
        """Busca un token válido (no revocado y no expirado)."""
        stmt = (
            select(RefreshToken)
            .where(RefreshToken.token == token)
            .where(RefreshToken.revocado == False)
            .where(RefreshToken.expires_at > datetime.now(timezone.utc))
        )
        return self.session.exec(stmt).first()
    
    def revoke(self, token: RefreshToken) -> None:
        """Marca un token como revocado."""
        token.revocado = True
        self.session.add(token)
        self.session.flush()
    
    def revoke_all_by_user(self, user_id: int) -> int:
        """Revoca todos los tokens de un usuario. Retorna la cantidad de tokens revocados."""
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .where(RefreshToken.revocado == False)
            .values(revocado=True)
        )
        result = self.session.exec(stmt)
        return result.rowcount
    
    def get_active_tokens_by_user(self, user_id: int) -> list[RefreshToken]:
        """Lista todos los tokens activos de un usuario."""
        stmt = (
            select(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .where(RefreshToken.revocado == False)
            .where(RefreshToken.expires_at > datetime.now(timezone.utc))
        )
        return list(self.session.exec(stmt).all())