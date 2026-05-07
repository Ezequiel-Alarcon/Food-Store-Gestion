"""app.modules.auth.schemas

Schemas Pydantic para el módulo de autenticación.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Schema para registro de usuario."""

    email: EmailStr = Field(
        ...,
        description="Email del usuario (único)",
        min_length=5,
        max_length=255,
    )
    password: str = Field(
        ...,
        description="Contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número)",
        min_length=8,
        max_length=128,
    )
    nombre: str = Field(
        ...,
        description="Nombre completo",
        min_length=1,
        max_length=100,
    )
    telefono: str | None = Field(
        default=None,
        description="Teléfono en formato E.164",
        max_length=20,
    )

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        """Normaliza email a minúsculas."""
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_not_whitespace(cls, v: str) -> str:
        """Verifica que la contraseña no sea solo whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("La contraseña no puede ser vacía")
        return v

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str) -> str:
        """Verifica que el nombre no sea solo whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío")
        return stripped

    @field_validator("telefono")
    @classmethod
    def telefono_cleanup(cls, v: str | None) -> str | None:
        """Limpia y valida formato de teléfono."""
        if v is None or v == "":
            return None
        # Remover espacios, guiones, paréntesis
        cleaned = "".join(c for c in v if c.isdigit() or c == "+")
        if len(cleaned) < 8:
            raise ValueError("Teléfono demasiado corto")
        return cleaned


class LoginRequest(BaseModel):
    """Schema para login."""

    email: EmailStr = Field(
        ...,
        description="Email del usuario",
    )
    password: str = Field(
        ...,
        description="Contraseña",
    )

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.lower().strip()


class TokenResponse(BaseModel):
    """Schema para respuesta de tokens."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Segundos hasta expiración")


class RefreshRequest(BaseModel):
    """Schema para refresh de token."""

    refresh_token: str = Field(..., description="Refresh token")


class ChangePasswordRequest(BaseModel):
    """Schema para cambiar contraseña."""

    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(
        ...,
        description="Nueva contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número)",
        min_length=8,
        max_length=128,
    )

    @field_validator("new_password")
    @classmethod
    def new_password_not_same(cls, v: str, info) -> str:
        """Verifica que la nueva contraseña no sea igual a la actual."""
        return v


class UpdateProfileRequest(BaseModel):
    """Schema para actualizar perfil propio."""

    nombre: str | None = Field(
        default=None,
        description="Nombre completo",
        min_length=1,
        max_length=100,
    )
    telefono: str | None = Field(
        default=None,
        description="Teléfono en formato E.164",
        max_length=20,
    )

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío")
        return stripped

    @field_validator("telefono")
    @classmethod
    def telefono_cleanup(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        cleaned = "".join(c for c in v if c.isdigit() or c == "+")
        if len(cleaned) < 8:
            raise ValueError("Teléfono demasiado corto")
        return cleaned