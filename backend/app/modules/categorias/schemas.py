"""app.modules.categorias.schemas

Schemas Pydantic para el módulo de categorías.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoriaCreate(BaseModel):
    """Schema para crear una categoría."""

    nombre: str = Field(
        ...,
        description="Nombre de la categoría",
        min_length=1,
        max_length=100,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción de la categoría",
        max_length=500,
    )
    categoria_padre_id: int | None = Field(
        default=None,
        description="ID de la categoría padre (para jerarquía)",
        gt=0,
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


class CategoriaUpdate(BaseModel):
    """Schema para actualizar una categoría."""

    nombre: str | None = Field(
        default=None,
        description="Nombre de la categoría",
        min_length=1,
        max_length=100,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción de la categoría",
        max_length=500,
    )
    categoria_padre_id: int | None = Field(
        default=None,
        description="ID de la categoría padre (null = raíz)",
    )
    activa: bool | None = Field(
        default=None,
        description="Si la categoría está activa",
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


class CategoriaResponse(BaseModel):
    """Schema para respuesta de categoría."""

    id: int
    nombre: str
    descripcion: str | None
    categoria_padre_id: int | None
    activa: bool

    model_config = ConfigDict(from_attributes=True)


class CategoriaTreeResponse(BaseModel):
    """Schema para respuesta de árbol de categorías."""

    id: int
    nombre: str
    descripcion: str | None
    activa: bool
    hijos: list["CategoriaTreeResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)