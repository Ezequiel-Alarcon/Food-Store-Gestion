"""app.modules.refreshtokens.router

Endpoints para gestión administrativa de refresh tokens.
Acceso restringido a ADMIN.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import SessionLocal
from app.core.deps import require_role
from app.core.uow import UnitOfWork
from app.modules.refreshtokens.repository import RefreshTokenRepository
from app.modules.refreshtokens.schemas import (
    BulkRevokeResponse,
    RefreshTokenListResponse,
    RefreshTokenRead,
    RevokeResponse,
)
from app.modules.refreshtokens.service import RefreshTokenService

router = APIRouter(prefix="/refreshtokens", tags=["refreshtokens"])


def _get_uow() -> UnitOfWork:
    """Factory de UnitOfWork para inyección."""
    return UnitOfWork(SessionLocal)


def _get_service() -> RefreshTokenService:
    """Factory de RefreshTokenService."""
    return RefreshTokenService(_get_uow())


# ── GET /refreshtokens/user/{user_id} ──────────────────────────────────

@router.get(
    "/user/{user_id}",
    response_model=RefreshTokenListResponse,
    summary="Listar tokens activos de un usuario",
    description="Retorna todos los refresh tokens activos (no revocados y no expirados) de un usuario.",
)
def list_user_tokens(
    user_id: int,
    current_user: Any = Depends(require_role("ADMIN")),
) -> RefreshTokenListResponse:
    """GET /refreshtokens/user/{user_id} — listar tokens activos."""
    with SessionLocal() as session:
        repo = RefreshTokenRepository(session)
        tokens = repo.get_active_tokens_by_user(user_id)
        return RefreshTokenListResponse(
            items=[RefreshTokenRead.model_validate(t) for t in tokens],
            count=len(tokens),
        )


# ── POST /refreshtokens/revoke/{token_id} ──────────────────────────────

@router.post(
    "/revoke/{token_id}",
    response_model=RevokeResponse,
    summary="Revocar un token individual",
    description="Revoca un refresh token específico por su ID.",
)
def revoke_token(
    token_id: int,
    current_user: Any = Depends(require_role("ADMIN")),
) -> RevokeResponse:
    """POST /refreshtokens/revoke/{token_id} — revocar token."""
    service = _get_service()
    token = service.revoke_by_id(token_id)

    return RevokeResponse(
        id=token.id,
        user_id=token.user_id,
        message="Token revocado correctamente",
    )


# ── DELETE /refreshtokens/user/{user_id}/all ───────────────────────────

@router.delete(
    "/user/{user_id}/all",
    response_model=BulkRevokeResponse,
    summary="Revocar todos los tokens de un usuario",
    description="Revoca todos los refresh tokens activos de un usuario.",
)
def revoke_all_user_tokens(
    user_id: int,
    current_user: Any = Depends(require_role("ADMIN")),
) -> BulkRevokeResponse:
    """DELETE /refreshtokens/user/{user_id}/all — revocar todos los tokens."""
    service = _get_service()
    revoked_count = service.revoke_all_by_user(user_id)
    return BulkRevokeResponse(
        user_id=user_id,
        revoked_count=revoked_count,
        message=f"Se revocaron {revoked_count} tokens del usuario {user_id}",
    )
