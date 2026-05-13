"""app.modules.usuarios.schemas

Schemas Pydantic para el módulo de administración de usuarios.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRead(BaseModel):
    """Schema para leer un usuario."""

    id: int = Field(..., description="ID único del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    nombre: str = Field(..., description="Nombre")
    apellido: str = Field(..., description="Apellido")
    rol: str = Field(..., description="Rol del usuario (ADMIN, STOCK, PEDIDOS, CLIENT)")
    telefono: Optional[str] = Field(None, description="Teléfono en formato E.164")
    activo: bool = Field(..., description="Si el usuario está activo")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")

    model_config = {"str_strip_whitespace": True}


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario (campos opcionales)."""

    nombre: Optional[str] = Field(
        default=None,
        description="Nombre",
        min_length=1,
        max_length=100,
    )
    apellido: Optional[str] = Field(
        default=None,
        description="Apellido",
        min_length=2,
        max_length=80,
    )
    rol: Optional[str] = Field(
        default=None,
        description="Rol del usuario (ADMIN, STOCK, PEDIDOS, CLIENT)",
        min_length=1,
        max_length=50,
    )
    telefono: Optional[str] = Field(
        default=None,
        description="Teléfono en formato E.164",
        max_length=20,
    )
    activo: Optional[bool] = Field(
        default=None,
        description="Si el usuario está activo",
    )

    model_config = {"str_strip_whitespace": True}

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío ni solo espacios")
        return stripped

    @field_validator("telefono")
    @classmethod
    def telefono_cleanup(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        cleaned = "".join(c for c in v if c.isdigit() or c == "+")
        if len(cleaned) < 8:
            raise ValueError("Teléfono demasiado corto")
        return cleaned


class UserListResponse(BaseModel):
    """Schema para respuesta de lista de usuarios."""

    id: int = Field(..., description="ID único del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    nombre: str = Field(..., description="Nombre")
    apellido: str = Field(..., description="Apellido")
    rol: str = Field(..., description="Rol del usuario (ADMIN, STOCK, PEDIDOS, CLIENT)")
    telefono: Optional[str] = Field(None, description="Teléfono en formato E.164")
    activo: bool = Field(..., description="Si el usuario está activo")
    created_at: Optional[str] = Field(None, description="Fecha de creación (ISO)")

    model_config = {"str_strip_whitespace": True}