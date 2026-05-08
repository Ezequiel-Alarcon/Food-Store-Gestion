"""
app.modules.ingredientes.model

Modelo SQLModel para ingredientes (alérgenos y componentes de productos).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Ingrediente(SQLModel, table=True):
    """
    Modelo de ingrediente para el catálogo de productos.

    Campos:
        - id: Identificador único (auto-incremental)
        - nombre: Nombre del ingrediente (max 100 chars, único entre no eliminados)
        - descripcion: Descripción opcional (max 500 chars)
        - es_alergeno: Flag que indica si es un alérgeno común
        - creado_en: Fecha de creación
        - actualizado_en: Fecha de última modificación
        - eliminado_en: Soft-delete (NULL = activo)
    """
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, primary_key=True, description="ID único")
    nombre: str = Field(
        max_length=100,
        index=True,
        description="Nombre del ingrediente",
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descripción del ingrediente",
    )
    es_alergeno: bool = Field(
        default=False,
        description="Flag de alérgeno común",
    )
    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación",
    )
    actualizado_en: Optional[datetime] = Field(
        default=None,
        description="Fecha de última modificación",
    )
    eliminado_en: Optional[datetime] = Field(
        default=None,
        description="Soft-delete (NULL = activo)",
    )

    def __repr__(self) -> str:
        return f"<Ingrediente(id={self.id}, nombre='{self.nombre}', es_alergeno={self.es_alergeno})>"