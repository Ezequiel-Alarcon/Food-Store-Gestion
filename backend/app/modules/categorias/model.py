"""
app.modules.categorias.model

Modelo SQLModel para categorías jerárquicas.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class Categoria(SQLModel, table=True):
    """
    Modelo de categoría para el catálogo de productos.

    Campos:
        - id: Identificador único (auto-incremental)
        - nombre: Nombre de la categoría (max 100 chars)
        - slug: Slug generado automáticamente desde nombre (único)
        - descripcion: Descripción opcional de la categoría
        - padre_id: FK auto-referencial al padre (NULL para categorías raíz)
        - orden: Campo para ordenamiento manual (drag & drop)
        - activa: Flag de soft-delete (True = activa, False = eliminada)
        - created_at: Fecha de creación
        - updated_at: Fecha de última modificación
    """
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True, description="ID único")
    nombre: str = Field(
        max_length=100,
        description="Nombre de la categoría",
    )
    slug: str = Field(
        unique=True,
        index=True,
        description="Slug generado automáticamente",
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción de la categoría",
    )
    padre_id: Optional[int] = Field(
        default=None,
        foreign_key="categorias.id",
        description="FK al padre (NULL = raíz)",
    )
    orden: int = Field(
        default=0,
        description="Orden para sorting manual",
    )
    activa: bool = Field(
        default=True,
        description="Flag de soft-delete",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de creación",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de última modificación",
    )

    # Relación auto-referencial para obtener hijos
    padre: Optional["Categoria"] = Relationship(
        sa_relationship_kwargs={
            "remote_side": "Categoria.id",
            "back_populates": "hijos",
        }
    )
    hijos: list["Categoria"] = Relationship(
        sa_relationship_kwargs={
            "back_populates": "padre",
        }
    )

    def __repr__(self) -> str:
        return f"<Categoria(id={self.id}, nombre='{self.nombre}', padre_id={self.padre_id})>"