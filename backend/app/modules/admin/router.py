"""app.modules.admin.router

Rutas para métricas del dashboard admin.
Acceso restringido a ADMIN y GESTOR.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from typing import Any

from app.core.deps import get_current_user, require_role
from app.modules.admin.schemas import (
    GeneralMetricsResponse,
    OrdersByStatusEntry,
    SalesChartResponse,
    TopProductEntry,
)
from app.modules.admin.service import AdminService


router = APIRouter(prefix="/admin", tags=["admin"])


def _get_service() -> AdminService:
    return AdminService()


# ── GET /admin/metrics/ ────────────────────────────────────────────────

@router.get(
    "/metrics/",
    response_model=GeneralMetricsResponse,
    summary="Métricas generales del dashboard",
    description="Retorna total_pedidos, total_revenue, ticket_promedio y total_clientes. "
                "Solo cuenta pedidos en estados ENTREGADO y CONFIRMADO.",
)
def get_general_metrics(
    current_user: Any = Depends(require_role("ADMIN", "GESTOR")),
    service: AdminService = Depends(_get_service),
) -> GeneralMetricsResponse:
    """GET /admin/metrics/ — métricas generales del dashboard."""
    return service.get_general_metrics()


# ── GET /admin/metrics/sales-chart/ ───────────────────────────────────

@router.get(
    "/metrics/sales-chart/",
    response_model=SalesChartResponse,
    summary="Datos del gráfico de ventas",
    description="Retorna revenue y count diario de los últimos 30 días. "
                "Solo incluye pedidos en estados ENTREGADO y CONFIRMADO.",
)
def get_sales_chart(
    current_user: Any = Depends(require_role("ADMIN", "GESTOR")),
    service: AdminService = Depends(_get_service),
) -> SalesChartResponse:
    """GET /admin/metrics/sales-chart/ — datos del gráfico de ventas."""
    return service.get_sales_chart(days=30)


# ── GET /admin/metrics/top-products/ ──────────────────────────────────

@router.get(
    "/metrics/top-products/",
    response_model=list[TopProductEntry],
    summary="Ranking de productos más vendidos",
    description="Retorna el top N productos más vendidos por cantidad total. "
                "Sin filtro temporal, solo productos activos.",
)
def get_top_products(
    current_user: Any = Depends(require_role("ADMIN", "GESTOR")),
    service: AdminService = Depends(_get_service),
) -> list[TopProductEntry]:
    """GET /admin/metrics/top-products/ — ranking de productos más vendidos."""
    return service.get_top_products(limit=10)


# ── GET /admin/metrics/orders-by-status/ ──────────────────────────────

@router.get(
    "/metrics/orders-by-status/",
    response_model=list[OrdersByStatusEntry],
    summary="Conteo de pedidos por estado",
    description="Retorna la cantidad de pedidos agrupados por estado_codigo.",
)
def get_orders_by_status(
    current_user: Any = Depends(require_role("ADMIN", "GESTOR")),
    service: AdminService = Depends(_get_service),
) -> list[OrdersByStatusEntry]:
    """GET /admin/metrics/orders-by-status/ — conteo de pedidos por estado."""
    return service.get_orders_by_status()