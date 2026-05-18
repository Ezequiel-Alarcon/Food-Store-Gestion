"""
app.modules.productos.model

Modelo SQLModel para productos del catálogo.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    """
    Modelo de producto para el catálogo de Food Store.

    Campos:
        - id: Identificador único (auto-incremental)
        - nombre: Nombre del producto (max 200 chars)
        - descripcion: Descripción opcional del producto (max 2000 chars)
        - precio: Precio del producto (decimal > 0)
        - imagen_url: URL de la imagen del producto
        - stock: Cantidad disponible en inventario
        - activo: Flag de disponibilidad (True = publicado)
        - eliminado_en: Timestamp de soft-delete (NULL = no eliminado)
        - creado_en: Fecha de creación
        - actualizado_en: Fecha de última modificación
    """
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True, description="ID único")
    nombre: str = Field(
        max_length=200,
        description="Nombre del producto",
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Descripción del producto",
    )
    precio: float = Field(
        description="Precio del producto (debe ser mayor a 0)",
    )
    imagen_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL de la imagen del producto",
    )
    stock: int = Field(
        default=0,
        description="Cantidad disponible en inventario",
    )
    activo: bool = Field(
        default=True,
        description="Flag de disponibilidad (soft-delete visual)",
    )
    eliminado_en: Optional[datetime] = Field(
        default=None,
        description="Timestamp de soft-delete (NULL = no eliminado)",
    )
    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación",
    )
    actualizado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de última modificación",
    )

    def __repr__(self) -> str:
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"


class ProductoCategoria(SQLModel, table=True):
    """
    Tabla de relación muchos-a-muchos entre productos y categorías.
    """
    __tablename__ = "producto_categorias"

    producto_id: int = Field(
        foreign_key="productos.id",
        primary_key=True,
        description="FK al producto",
    )
    categoria_id: int = Field(
        foreign_key="categorias.id",
        primary_key=True,
        description="FK a la categoría",
    )
    es_principal: bool = Field(default=False, description="Categoría principal del producto")


class ProductoIngrediente(SQLModel, table=True):
    """
    Tabla de relación muchos-a-muchos entre productos e ingredientes.
    """
    __tablename__ = "producto_ingredientes"

    producto_id: int = Field(
        foreign_key="productos.id",
        primary_key=True,
        description="FK al producto",
    )
    ingrediente_id: int = Field(
        foreign_key="ingredientes.id",
        primary_key=True,
        description="FK al ingrediente",
    )
    es_removible: bool = Field(default=False, description="Indica si el ingrediente se puede excluir del pedido")