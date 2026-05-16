"""app.modules.admin.service

Servicio para métricas del dashboard admin.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.modules.admin.repository import AdminRepository
from app.modules.admin.schemas import (
    GeneralMetricsResponse,
    OrdersByStatusEntry,
    SalesChartEntry,
    SalesChartResponse,
    TopProductEntry,
)


class AdminService:
    """Servicio para métricas del dashboard admin."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = AdminRepository(self.session)

    def get_general_metrics(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> GeneralMetricsResponse:
        """Retorna métricas generales del dashboard.

        Maneja resultados vacíos: si no hay pedidos, retorna ceros.
        """
        data = self.repo.get_general_metrics(desde=desde, hasta=hasta)
        return GeneralMetricsResponse(**data)

    def get_sales_chart(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> SalesChartResponse:
        """Retorna datos del gráfico de ventas para el rango especificado.

        Si no se pasan desde/hasta, usa default últimos 30 días.
        Maneja resultados vacíos: retorna lista vacía con dias=30.
        """
        datos = self.repo.get_sales_chart(desde=desde, hasta=hasta)
        entries = [
            SalesChartEntry(
                fecha=row["fecha"],
                total_pedidos=row["total_pedidos"],
                revenue=row["revenue"],
            )
            for row in datos
        ]
        dias = 30 if desde is None else None
        if desde and hasta:
            dias = (hasta - desde).days
        elif desde:
            dias = (datetime.now() - desde).days
        return SalesChartResponse(datos=entries, dias=dias if dias is not None else 30)

    def get_top_products(
        self,
        limit: int = 10,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[TopProductEntry]:
        """Retorna ranking de productos más vendidos.

        Maneja resultados vacíos: retorna lista vacía.
        """
        datos = self.repo.get_top_products(limit=limit, desde=desde, hasta=hasta)
        return [
            TopProductEntry(
                producto_id=row["producto_id"],
                nombre=row["nombre"],
                cantidad_vendida=row["cantidad_vendida"],
            )
            for row in datos
        ]

    def get_orders_by_status(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[OrdersByStatusEntry]:
        """Retorna conteo de pedidos por estado.

        Maneja resultados vacíos: retorna lista vacía.
        """
        datos = self.repo.get_orders_by_status(desde=desde, hasta=hasta)
        return [
            OrdersByStatusEntry(
                estado_codigo=row["estado_codigo"],
                cantidad=row["cantidad"],
            )
            for row in datos
        ]

    def get_total_usuarios_registrados(self) -> int:
        """Retorna el total de usuarios registrados en el sistema."""
        return self.repo.get_total_usuarios_registrados()
