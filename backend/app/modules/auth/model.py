"""
app.modules.auth.model

Modelos SQLModel para autenticación y usuarios.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class RolEnum(str, Enum):
    """Roles predefinidos del sistema (4 roles RBAC)."""
    ADMIN = "ADMIN"
    STOCK = "STOCK"      # Gestor de Stock
    PEDIDOS = "PEDIDOS"  # Gestor de Pedidos
    CLIENT = "CLIENT"


class Usuario(SQLModel, table=True):
    """
    Modelo de usuario para autenticación y gestión de identidad.
    
    Campos:
        - id: Identificador único (autoincremental)
        - email: Email único del usuario
        - nombre: Nombre
        - apellido: Apellido
        - password_hash: Hash de la contraseña (nunca almacenar password plano)
        - rol: Rol del usuario (ADMIN, STOCK, PEDIDOS, CLIENT)
        - telefono: Teléfono opcional en formato E.164
        - activo: Indica si el usuario está activo (para soft delete)
        - created_at: Fecha de creación
        - updated_at: Fecha de última modificación
    """
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, description="Email único del usuario")
    nombre: str = Field(description="Nombre del usuario")
    apellido: str = Field(description="Apellido del usuario")
    password_hash: str = Field(description="Hash bcrypt de la contraseña")
    rol: RolEnum = Field(default=RolEnum.CLIENT, description="Rol del usuario")
    telefono: Optional[str] = Field(default=None, description="Teléfono en formato E.164")
    activo: bool = Field(default=True, description="Usuario activo (soft delete)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Fecha de creación")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Fecha de última modificación")

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, email='{self.email}', rol='{self.rol}')>"