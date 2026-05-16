"""app.modules.sucursales.schemas

Schemas Pydantic para sucursales.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SucursalCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120)

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede ser vacío")
        return v


class SucursalUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    activa: bool | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede ser vacío")
        return v


class SucursalResponse(BaseModel):
    id: int
    nombre: str
    activa: bool

    model_config = ConfigDict(from_attributes=True)
