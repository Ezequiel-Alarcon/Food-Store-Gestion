"""app.modules.admin.service

Servicio para métricas del dashboard admin.
"""
from __future__ import annotations

from typing import Any

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

    def __init__(self, repository: AdminRepository | None = None):
        self._repository = repository

    @property
    def repo(self) -> AdminRepository:
        if self._repository is None:
            from app.core.database import SessionLocal

            self._repository = AdminRepository(SessionLocal())
        return self._repository

    def get_general_metrics(self) -> GeneralMetricsResponse:
        """Retorna métricas generales del dashboard.

        Maneja resultados vacíos: si no hay pedidos, retorna ceros.
        """
        data = self.repo.get_general_metrics()
        return GeneralMetricsResponse(**data)

    def get_sales_chart(self, days: int = 30) -> SalesChartResponse:
        """Retorna datos del gráfico de ventas para los últimos `days` días.

        Maneja resultados vacíos: retorna lista vacía con dias=N.
        """
        datos = self.repo.get_sales_chart(days)
        entries = [
            SalesChartEntry(
                fecha=row["fecha"],
                total_pedidos=row["total_pedidos"],
                revenue=row["revenue"],
            )
            for row in datos
        ]
        return SalesChartResponse(datos=entries, dias=days)

    def get_top_products(self, limit: int = 10) -> list[TopProductEntry]:
        """Retorna ranking de productos más vendidos.

        Maneja resultados vacíos: retorna lista vacía.
        """
        datos = self.repo.get_top_products(limit)
        return [
            TopProductEntry(
                producto_id=row["producto_id"],
                nombre=row["nombre"],
                cantidad_vendida=row["cantidad_vendida"],
            )
            for row in datos
        ]

    def get_orders_by_status(self) -> list[OrdersByStatusEntry]:
        """Retorna conteo de pedidos por estado.

        Maneja resultados vacíos: retorna lista vacía.
        """
        datos = self.repo.get_orders_by_status()
        return [
            OrdersByStatusEntry(
                estado_codigo=row["estado_codigo"],
                cantidad=row["cantidad"],
            )
            for row in datos
        ]