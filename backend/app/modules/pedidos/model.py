"""app.modules.pedidos.model

Modelos SQLModel para pedidos, items y FSM de estados.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Integer as SAInt
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel


class EstadoPedido(SQLModel, table=True):
    """Estado de la FSM de pedidos (tabla de lookup, seeded)."""
    __tablename__ = "estados_pedido"

    codigo: str = Field(primary_key=True, max_length=30)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    orden: int = Field(default=0)
    es_terminal: bool = Field(default=False)


class ActorTipo(str, Enum):
    USUARIO = "USUARIO"
    SISTEMA = "SISTEMA"


class Pedido(SQLModel, table=True):
    """Cabecera del pedido con snapshot de dirección."""
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="usuarios.id", index=True)
    estado_codigo: str = Field(
        foreign_key="estados_pedido.codigo",
        default="PENDIENTE",
        index=True,
    )

    # Snapshot dirección al momento de la compra (RN-PE03)
    direccion_calle: str = Field(max_length=120)
    direccion_numero: str = Field(max_length=30)
    direccion_piso_depto: Optional[str] = Field(default=None, max_length=60)
    direccion_ciudad: str = Field(max_length=120)
    direccion_provincia: str = Field(max_length=120)
    direccion_codigo_postal: Optional[str] = Field(default=None, max_length=20)
    direccion_pais: str = Field(max_length=120, default="Argentina")
    direccion_referencias: Optional[str] = Field(default=None, max_length=500)

    total: float = Field(description="Suma de subtotales + costo_envio")
    costo_envio: float = Field(default=0.0)

    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actualizado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, estado='{self.estado_codigo}')>"


class DetallePedido(SQLModel, table=True):
    """Línea de pedido con precio snapshot y exclusiones de ingredientes."""
    __tablename__ = "detalle_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", index=True)
    producto_id: int = Field(foreign_key="productos.id")
    cantidad: int = Field(ge=1)
    precio_unitario: float = Field(description="Precio snapshot al momento de la compra (RN-PE02)")
    # INTEGER[] — almacena IDs de ingredientes excluidos (RN-PE07)
    exclusiones: list = Field(
        default=[],
        sa_column=Column("exclusiones", ARRAY(SAInt), nullable=False, server_default="{}"),
    )


class HistorialEstadoPedido(SQLModel, table=True):
    """Registro append-only de transiciones de estado (RN-DA05, RN-FS07)."""
    __tablename__ = "historial_estado_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", index=True)
    estado_anterior_codigo: Optional[str] = Field(
        default=None,
        foreign_key="estados_pedido.codigo",
    )
    estado_nuevo_codigo: str = Field(foreign_key="estados_pedido.codigo")
    actor_id: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    actor_tipo: str = Field(default=ActorTipo.USUARIO.value, max_length=20)
    motivo: Optional[str] = Field(default=None)
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
