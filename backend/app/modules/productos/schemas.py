"""app.modules.productos.schemas

Schemas Pydantic para el módulo de productos.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductoCreate(BaseModel):
    """Schema para crear un producto."""

    nombre: str = Field(
        ...,
        description="Nombre del producto",
        min_length=1,
        max_length=200,
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción del producto",
        max_length=2000,
    )
    precio: Decimal = Field(
        ...,
        description="Precio del producto (debe ser mayor a 0)",
        gt=0,
    )
    imagen_url: Optional[str] = Field(
        default=None,
        description="URL de la imagen del producto",
        max_length=500,
    )
    stock: int = Field(
        default=0,
        description="Cantidad disponible en inventario",
        ge=0,
    )
    categoria_ids: list[int] = Field(
        default_factory=list,
        description="IDs de categorías asociadas",
    )
    ingrediente_ids: list[int] = Field(
        default_factory=list,
        description="IDs de ingredientes asociados",
    )
    activo: bool = Field(
        default=True,
        description="Si el producto está activo/publicado",
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
    def descripcion_cleanup(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return v.strip() or None


class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto."""

    nombre: Optional[str] = Field(
        default=None,
        description="Nombre del producto",
        min_length=1,
        max_length=200,
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción del producto",
        max_length=2000,
    )
    precio: Optional[Decimal] = Field(
        default=None,
        description="Precio del producto (debe ser mayor a 0)",
        gt=0,
    )
    imagen_url: Optional[str] = Field(
        default=None,
        description="URL de la imagen del producto",
        max_length=500,
    )
    stock: Optional[int] = Field(
        default=None,
        description="Cantidad disponible en inventario",
        ge=0,
    )
    categoria_ids: Optional[list[int]] = Field(
        default=None,
        description="IDs de categorías asociadas",
    )
    ingrediente_ids: Optional[list[int]] = Field(
        default=None,
        description="IDs de ingredientes asociados",
    )
    activo: Optional[bool] = Field(
        default=None,
        description="Si el producto está activo/publicado",
    )

    @field_validator("nombre")
    @classmethod
    def nombre_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede ser vacío ni solo espacios")
        return stripped

    @field_validator("descripcion")
    @classmethod
    def descripcion_cleanup(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return v.strip() or None


class CategoriaSimple(BaseModel):
    """Schema minimal de categoría para respuestas anidadas."""

    id: int
    nombre: str
    es_principal: bool = False

    model_config = ConfigDict(from_attributes=True)


class IngredienteSimple(BaseModel):
    """Schema minimal de ingrediente para respuestas anidadas."""

    id: int
    nombre: str
    es_removible: bool = False

    model_config = ConfigDict(from_attributes=True)


class ProductoResponse(BaseModel):
    """Schema para respuesta de producto (detalle completo)."""

    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    imagen_url: Optional[str]
    stock: int
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
    categorias: list[CategoriaSimple] = Field(default_factory=list)
    ingredientes: list[IngredienteSimple] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProductoListResponse(BaseModel):
    """Schema para respuesta de lista de productos."""

    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    imagen_url: Optional[str]
    stock: int
    activo: bool
    categorias: list[CategoriaSimple] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProductoStockUpdate(BaseModel):
    """Schema para actualizar el stock de un producto."""

    stock: int = Field(
        ...,
        description="Nueva cantidad de stock",
        ge=0,
    )
    operacion: str = Field(
        ...,
        description="Tipo de operación: 'set' (setear), 'add' (sumar), 'subtract' (restar)",
        pattern="^(set|add|subtract)$",
    )


class ProductoCatalogoResponse(BaseModel):
    """Schema para respuesta del catálogo público."""

    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    imagen_url: Optional[str]
    disponible: bool
    categorias: list[CategoriaSimple] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class PaginatedProductoResponse(BaseModel):
    """Schema para respuesta paginada de productos."""

    items: list[Any]
    total: int
    skip: int
    limit: int