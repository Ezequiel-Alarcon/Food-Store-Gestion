"""
app.modules.ingredientes.schemas

Schemas Pydantic para el módulo de ingredientes.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class IngredienteCreate(BaseModel):
    """Schema para crear un ingrediente."""

    nombre: str = Field(
        ...,
        description="Nombre del ingrediente",
        min_length=1,
        max_length=100,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción del ingrediente",
        max_length=500,
    )
    es_alergeno: bool = Field(
        default=False,
        description="Flag de alérgeno común",
    )

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío ni solo espacios")
        return stripped

    @field_validator("descripcion")
    @classmethod
    def descripcion_cleanup(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip() or None


class IngredienteUpdate(BaseModel):
    """Schema para actualizar un ingrediente (PATCH - todos los campos opcionales)."""

    nombre: str | None = Field(
        default=None,
        description="Nombre del ingrediente",
        min_length=1,
        max_length=100,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción del ingrediente",
        max_length=500,
    )
    es_alergeno: bool | None = Field(
        default=None,
        description="Flag de alérgeno común",
    )

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío ni solo espacios")
        return stripped

    @field_validator("descripcion")
    @classmethod
    def descripcion_cleanup(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip() or None


class IngredienteResponse(BaseModel):
    """Schema para respuesta de ingrediente."""

    id: int
    nombre: str
    descripcion: str | None
    es_alergeno: bool
    creado_en: str
    actualizado_en: str | None

    model_config = ConfigDict(from_attributes=True)


class IngredienteListResponse(BaseModel):
    """Schema para respuesta de listado de ingredientes."""

    id: int
    nombre: str
    descripcion: str | None
    es_alergeno: bool
    creado_en: str
    actualizado_en: str | None

    model_config = ConfigDict(from_attributes=True)