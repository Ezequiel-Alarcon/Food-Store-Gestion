"""app.modules.admin.schemas

Schemas Pydantic v2 para métricas del dashboard admin.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GeneralMetricsResponse(BaseModel):
    """Métricas generales del dashboard."""
    model_config = {"str_strip_whitespace": True}

    total_pedidos: int = Field(..., description="Total de pedidos completados (ENTREGADO + CONFIRMADO)")
    total_revenue: float = Field(..., description="Suma de montos de pedidos completados")
    ticket_promedio: float = Field(..., description="Revenue / total_pedidos, 0 si no hay pedidos")
    total_clientes: int = Field(..., description="Cantidad de clientes únicos con pedidos")
    total_usuarios: int = Field(..., description="Total de usuarios registrados en el sistema")


class SalesChartEntry(BaseModel):
    """Una entrada del gráfico de ventas por día."""
    model_config = {"str_strip_whitespace": True}

    fecha: datetime = Field(..., description="Fecha del día (truncada a día)")
    total_pedidos: int = Field(..., description="Cantidad de pedidos ese día")
    revenue: float = Field(..., description="Suma de montos ese día")


class SalesChartResponse(BaseModel):
    """Respuesta del endpoint de sales chart."""
    model_config = {"str_strip_whitespace": True}

    datos: list[SalesChartEntry] = Field(..., description="Lista de entradas diarias")
    dias: int = Field(..., description="Cantidad de días en el rango")


class TopProductEntry(BaseModel):
    """Una entrada en el ranking de productos más vendidos."""
    model_config = {"str_strip_whitespace": True}

    producto_id: int = Field(..., description="ID del producto")
    nombre: str = Field(..., description="Nombre del producto")
    cantidad_vendida: int = Field(..., description="Total de unidades vendidas")


class OrdersByStatusEntry(BaseModel):
    """Una entrada en el conteo de pedidos por estado."""
    model_config = {"str_strip_whitespace": True}

    estado_codigo: str = Field(..., description="Código del estado del pedido")
    cantidad: int = Field(..., description="Cantidad de pedidos en ese estado")


class PedidoDetailItem(BaseModel):
    """Un item dentro del detalle de un pedido."""
    model_config = {"str_strip_whitespace": True}

    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    exclusiones: list = Field(default_factory=list)


class PedidoDetailResponse(BaseModel):
    """Respuesta del endpoint de detalle de pedido."""
    model_config = {"str_strip_whitespace": True}

    id: int
    cliente_id: int
    estado_codigo: str
    cliente_email: str | None
    cliente_nombre: str | None
    cliente_apellido: str | None
    direccion_calle: str | None
    direccion_numero: str | None
    direccion_piso_depto: str | None
    direccion_ciudad: str | None
    direccion_provincia: str | None
    direccion_codigo_postal: str | None
    direccion_pais: str | None
    direccion_referencias: str | None
    total: float
    costo_envio: float | None
    items: list[PedidoDetailItem]
    creado_en: datetime | None
    actualizado_en: datetime | None


class PedidoHistorialEntry(BaseModel):
    """Una entrada en el historial de estados de un pedido."""
    model_config = {"str_strip_whitespace": True}

    id: int
    estado_anterior_codigo: str | None
    estado_nuevo_codigo: str
    actor_id: int | None
    actor_tipo: str | None
    motivo: str | None
    creado_en: datetime | None
