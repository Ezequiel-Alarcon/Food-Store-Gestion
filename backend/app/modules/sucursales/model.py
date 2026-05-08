"""app.modules.sucursales.model

Modelo SQLModel para sucursales (puntos de retiro).
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Sucursal(SQLModel, table=True):
    """Sucursal.

    Nota: modelo minimo para soportar branch_addresses.
    """

    __tablename__ = "sucursales"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=120, index=True)
    activa: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
