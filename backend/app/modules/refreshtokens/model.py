"""
app.modules.refreshtokens.model

Modelos SQLModel para refresh tokens.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class RefreshToken(SQLModel, table=True):
    """
    Modelo de refresh token para renovación de access tokens.
    
    Campos:
        - id: Identificador único
        - user_id: FK al usuario propietario del token
        - token: El JWT refresh token (puede храниться hashed para mayor seguridad)
        - revocado: Indica si el token ha sido revocdo
        - expires_at: Fecha de expiración del token
        - created_at: Fecha de creación
    """
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="usuarios.id", description="FK al usuario")
    token: str = Field(index=True, description="JWT refresh token")
    revocado: bool = Field(default=False, description="Token revocado")
    expires_at: datetime = Field(description="Fecha de expiración")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Fecha de creación")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revocado={self.revocado})>"