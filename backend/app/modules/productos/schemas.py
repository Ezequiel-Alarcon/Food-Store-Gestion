"""app.modules.productos.schemas

Schemas Pydantic para el módulo de productos.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ProductoCreate(BaseModel):
    """Schema para crear un producto."""

    nombre: str = Field(
        ...,
        description="Nombre del producto",
        min_length=1,
        max_length=200,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción del producto",
        max_length=1000,
    )
    precio: float = Field(
        ...,
        description="Precio del producto",
        gt=0,
    )
    stock: int = Field(
        default=0,
        description="Cantidad en stock",
        ge=0,
    )
    categoria_id: int | None = Field(
        default=None,
        description="ID de la categoría",
        gt=0,
    )

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío")
        return stripped

    @field_validator("descripcion")
    @classmethod
    def descripcion_cleanup(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip() or None


class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto."""

    nombre: str | None = Field(
        default=None,
        description="Nombre del producto",
        min_length=1,
        max_length=200,
    )
    descripcion: str | None = Field(
        default=None,
        description="Descripción del producto",
        max_length=1000,
    )
    precio: float | None = Field(
        default=None,
        description="Precio del producto",
        gt=0,
    )
    stock: int | None = Field(
        default=None,
        description="Cantidad en stock",
        ge=0,
    )
    categoria_id: int | None = Field(
        default=None,
        description="ID de la categoría",
        gt=0,
    )
    activo: bool | None = Field(
        default=None,
        description="Si el producto está activo",
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

    @field_validator("descripcion")
    @classmethod
    def descripcion_cleanup(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip() or None


class ProductoResponse(BaseModel):
    """Schema para respuesta de producto."""

    id: int
    nombre: str
    descripcion: str | None
    precio: float
    stock: int
    categoria_id: int | None
    activo: bool

    class Config:
        from_attributes = True