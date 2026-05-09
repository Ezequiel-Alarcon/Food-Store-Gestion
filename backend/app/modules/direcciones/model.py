"""app.modules.direcciones.model

Modelos SQLModel para direcciones de usuario y de sucursal.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserAddress(SQLModel, table=True):
    __tablename__ = "user_addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="usuarios.id", index=True)

    etiqueta: Optional[str] = Field(default=None, max_length=60)
    calle: str = Field(min_length=1, max_length=120)
    numero: str = Field(min_length=1, max_length=30)
    piso_depto: Optional[str] = Field(default=None, max_length=60)
    ciudad: str = Field(min_length=1, max_length=120)
    provincia: str = Field(min_length=1, max_length=120)
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    pais: str = Field(min_length=1, max_length=120)
    referencias: Optional[str] = Field(default=None, max_length=500)

    is_default: bool = Field(default=False)
    activa: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BranchAddress(SQLModel, table=True):
    __tablename__ = "branch_addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="sucursales.id", index=True)

    calle: str = Field(min_length=1, max_length=120)
    numero: str = Field(min_length=1, max_length=30)
    piso_depto: Optional[str] = Field(default=None, max_length=60)
    ciudad: str = Field(min_length=1, max_length=120)
    provincia: str = Field(min_length=1, max_length=120)
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    pais: str = Field(min_length=1, max_length=120)
    referencias: Optional[str] = Field(default=None, max_length=500)

    activa: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
