"""app.modules.pedidos.schemas

Schemas Pydantic v2 para el módulo de pedidos.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int
    exclusiones: list[int] = []

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v


class PedidoCreate(BaseModel):
    direccion_id: int
    items: list[PedidoItemCreate]

    @field_validator("items")
    @classmethod
    def items_no_vacio(cls, v: list) -> list:
        if not v:
            raise ValueError("El pedido debe tener al menos un ítem")
        return v


class DetallePedidoRead(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    exclusiones: list[int]

    model_config = {"from_attributes": True}


class PedidoRead(BaseModel):
    id: int
    cliente_id: int
    estado_codigo: str
    direccion_calle: str
    direccion_numero: str
    direccion_piso_depto: Optional[str]
    direccion_ciudad: str
    direccion_provincia: str
    direccion_codigo_postal: Optional[str]
    direccion_pais: str
    direccion_referencias: Optional[str]
    total: float
    costo_envio: float
    items: list[DetallePedidoRead] = []
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class EstadoTransicionCreate(BaseModel):
    nuevo_estado: str
    motivo: Optional[str] = None

    @model_validator(mode="after")
    def motivo_requerido_para_cancelar(self) -> "EstadoTransicionCreate":
        if self.nuevo_estado == "CANCELADO" and not self.motivo:
            raise ValueError("El motivo es obligatorio para cancelaciones")
        return self


class HistorialEstadoRead(BaseModel):
    id: int
    estado_anterior_codigo: Optional[str]
    estado_nuevo_codigo: str
    actor_id: Optional[int]
    actor_tipo: str
    motivo: Optional[str]
    creado_en: datetime

    model_config = {"from_attributes": True}
