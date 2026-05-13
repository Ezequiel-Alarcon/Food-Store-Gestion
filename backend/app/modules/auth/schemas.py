"""app.modules.auth.schemas

Schemas Pydantic para el módulo de autenticación.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


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
        description="Nombre",
        min_length=1,
        max_length=100,
    )
    apellido: str = Field(
        ...,
        description="Apellido",
        min_length=2,
        max_length=80,
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
        """Verifica que la contraseña no sea solo whitespace y retorna stripped."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("La contraseña no puede ser vacía")
        return stripped

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        """Verifica complejidad: al menos 1 mayúscula y 1 número."""
        v = v.strip()
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str) -> str:
        """Verifica que el nombre no sea solo whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío")
        return stripped

    @field_validator("apellido")
    @classmethod
    def apellido_not_whitespace(cls, v: str) -> str:
        """Verifica que el apellido no sea solo whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El apellido no puede ser vacío")
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


class MessageResponse(BaseModel):
    """Schema genérico para respuestas con mensaje."""

    message: str = Field(..., description="Mensaje de respuesta")


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
        current = info.data.get("current_password") if info.data else None
        if current is not None and v == current:
            raise ValueError("La nueva contraseña no puede ser igual a la actual")
        return v

    @field_validator("new_password")
    @classmethod
    def new_password_complexity(cls, v: str) -> str:
        """Verifica complejidad: al menos 1 mayúscula y 1 número."""
        v = v.strip()
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v


class UpdateProfileRequest(BaseModel):
    """Schema para actualizar perfil propio."""

    nombre: str | None = Field(
        default=None,
        description="Nombre",
        min_length=1,
        max_length=100,
    )
    apellido: str | None = Field(
        default=None,
        description="Apellido",
        min_length=2,
        max_length=80,
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

    @field_validator("apellido")
    @classmethod
    def apellido_not_whitespace(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("El apellido no puede ser vacío")
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