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