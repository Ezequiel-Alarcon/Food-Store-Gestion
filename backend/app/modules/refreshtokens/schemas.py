"""app.modules.refreshtokens.schemas

Schemas Pydantic para el módulo de refresh tokens.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenRead(BaseModel):
    """Schema de lectura para refresh token."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID del token")
    user_id: int = Field(..., description="ID del usuario propietario")
    expires_at: datetime = Field(..., description="Fecha de expiración")
    created_at: datetime = Field(..., description="Fecha de creación")
    revocado: bool = Field(..., description="Indica si fue revocado")


class RefreshTokenListResponse(BaseModel):
    """Respuesta paginada para listar tokens."""

    items: list[RefreshTokenRead] = Field(..., description="Lista de tokens activos")
    count: int = Field(..., description="Cantidad total de tokens")


class RevokeResponse(BaseModel):
    """Respuesta para revocación individual."""

    id: int = Field(..., description="ID del token revocado")
    user_id: int = Field(..., description="ID del usuario propietario")
    message: str = Field(..., description="Mensaje de confirmación")


class BulkRevokeResponse(BaseModel):
    """Respuesta para revocación masiva por usuario."""

    user_id: int = Field(..., description="ID del usuario")
    revoked_count: int = Field(..., description="Cantidad de tokens revocados")
    message: str = Field(..., description="Mensaje de confirmación")
