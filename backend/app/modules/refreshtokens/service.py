"""app.modules.refreshtokens.service

Servicio para gestión de refresh tokens.
Usa Unit of Work para transacciones de escritura.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from app.core.config import get_settings

if TYPE_CHECKING:
    from app.core.uow import UnitOfWork

from app.modules.refreshtokens.model import RefreshToken
from app.modules.refreshtokens.repository import RefreshTokenRepository

settings = get_settings()


class RefreshTokenService:
    """
    Servicio de refresh tokens.

    Opera con RefreshTokenRepository a través de UnitOfWork.
    """

    def __init__(self, uow: "UnitOfWork"):
        self.uow = uow

    def create(self, user_id: int, token: str) -> RefreshToken:
        """Crea un nuevo refresh token."""
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            result = repo.create(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
            )
            return result

    def get_valid(self, session, token: str) -> RefreshToken | None:
        """Busca un token válido (solo lectura, no usa UoW)."""
        repo = RefreshTokenRepository(session)
        return repo.get_valid_token(token)

    def revoke(self, token: RefreshToken) -> None:
        """Revoca un token."""
        with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            repo.revoke(token)

    def revoke_by_id(self, token_id: int) -> RefreshToken:
        """Revoca un token por ID dentro de una sola transacción.

        Raises:
            HTTPException 404: Token no encontrado.
            HTTPException 400: Token ya revocado.
        """
        from fastapi import HTTPException, status

        with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            token = repo.get_by_id(token_id)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Token no encontrado",
                )
            if token.revocado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El token ya está revocado",
                )
            repo.revoke(token)
            return token

    def revoke_all_by_user(self, user_id: int) -> int:
        """Revoca todos los tokens de un usuario. Retorna cantidad revocada."""
        with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            return repo.revoke_all_by_user(user_id)
