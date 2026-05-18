"""app.modules.admin.router

Rutas para métricas del dashboard admin.
Acceso restringido a ADMIN, STOCK y PEDIDOS.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from sqlmodel import Session, select

from app.core.deps import require_role
from app.core.database import get_session, SessionLocal
from app.modules.admin.schemas import (
    GeneralMetricsResponse,
    OrdersByStatusEntry,
    PedidoDetailResponse,
    PedidoHistorialEntry,
    SalesChartResponse,
    TopProductEntry,
)
from app.modules.admin.service import AdminService
from app.modules.pedidos.schemas import PaginatedPedidosResponse
from app.modules.pedidos.service import PedidosService
from app.modules.pedidos.model import DetallePedido, HistorialEstadoPedido, Pedido
from app.modules.auth.model import Usuario


router = APIRouter(prefix="/admin", tags=["admin"])


def _get_service(session: Session = Depends(get_session)) -> AdminService:
    return AdminService(session)


# ── GET /admin/metrics/ ────────────────────────────────────────────────

@router.get(
    "/metrics/",
    response_model=GeneralMetricsResponse,
    summary="Métricas generales del dashboard",
    description="Retorna total_pedidos, total_revenue, ticket_promedio y total_clientes. "
                "Solo cuenta pedidos en estados ENTREGADO y CONFIRMADO.",
)
def get_general_metrics(
    desde: datetime | None = None,
    hasta: datetime | None = None,
    current_user: Any = Depends(require_role("ADMIN")),
    service: AdminService = Depends(_get_service),
) -> GeneralMetricsResponse:
    """GET /admin/metrics/ — métricas generales del dashboard."""
    return service.get_general_metrics(desde=desde, hasta=hasta)


# ── GET /admin/metrics/sales-chart/ ───────────────────────────────────

@router.get(
    "/metrics/sales-chart/",
    response_model=SalesChartResponse,
    summary="Datos del gráfico de ventas",
    description="Retorna revenue y count diario del rango especificado. "
                "Si no se pasan desde/hasta, usa últimos 30 días. "
                "Solo incluye pedidos en estados ENTREGADO y CONFIRMADO.",
)
def get_sales_chart(
    desde: datetime | None = None,
    hasta: datetime | None = None,
    current_user: Any = Depends(require_role("ADMIN")),
    service: AdminService = Depends(_get_service),
) -> SalesChartResponse:
    """GET /admin/metrics/sales-chart/ — datos del gráfico de ventas."""
    return service.get_sales_chart(desde=desde, hasta=hasta)


# ── GET /admin/metrics/top-products/ ──────────────────────────────────

@router.get(
    "/metrics/top-products/",
    response_model=list[TopProductEntry],
    summary="Ranking de productos más vendidos",
    description="Retorna el top N productos más vendidos por cantidad total. "
                "Sin filtro temporal por defecto, solo productos activos.",
)
def get_top_products(
    limit: int = 10,
    desde: datetime | None = None,
    hasta: datetime | None = None,
    current_user: Any = Depends(require_role("ADMIN")),
    service: AdminService = Depends(_get_service),
) -> list[TopProductEntry]:
    """GET /admin/metrics/top-products/ — ranking de productos más vendidos."""
    return service.get_top_products(limit=limit, desde=desde, hasta=hasta)


# ── GET /admin/metrics/orders-by-status/ ──────────────────────────────

@router.get(
    "/metrics/orders-by-status/",
    response_model=list[OrdersByStatusEntry],
    summary="Conteo de pedidos por estado",
    description="Retorna la cantidad de pedidos agrupados por estado_codigo.",
)
def get_orders_by_status(
    desde: datetime | None = None,
    hasta: datetime | None = None,
    current_user: Any = Depends(require_role("ADMIN")),
    service: AdminService = Depends(_get_service),
) -> list[OrdersByStatusEntry]:
    """GET /admin/metrics/orders-by-status/ — conteo de pedidos por estado."""
    return service.get_orders_by_status(desde=desde, hasta=hasta)


# ── GET /admin/pedidos/ ─────────────────────────────────────────────────

@router.get(
    "/pedidos/",
    response_model=PaginatedPedidosResponse,
    summary="Listar todos los pedidos",
    description="Lista todos los pedidos del sistema con filtros opcionales.",
)
def list_pedidos(
    page: int = 1,
    size: int = 20,
    estado: str | None = None,
    q: str | None = None,
    current_user: Any = Depends(require_role("ADMIN", "PEDIDOS")),
) -> PaginatedPedidosResponse:
    """GET /admin/pedidos/ — listar pedidos con filtros."""
    service = PedidosService()
    return service.list_pedidos_for_admin(
        page=page,
        size=size,
        estado=estado,
        q=q,
    )


# ── GET /admin/pedidos/{id}/ ────────────────────────────────────────────

@router.get(
    "/pedidos/{pedido_id}/",
    response_model=PedidoDetailResponse,
    summary="Ver detalle de un pedido",
    description="Retorna el detalle completo de un pedido.",
)
def get_pedido(
    pedido_id: int,
    current_user: Any = Depends(require_role("ADMIN", "PEDIDOS")),
) -> PedidoDetailResponse:
    """GET /admin/pedidos/{id}/ — detalle de un pedido."""
    with SessionLocal() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        # Obtener datos del cliente
        cliente = session.get(Usuario, pedido.cliente_id)

        # Obtener items del pedido
        items_stmt = select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        items = session.exec(items_stmt).all()

        items_data = [
            PedidoDetailItem(
                id=item.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                exclusiones=item.exclusiones or [],
            )
            for item in items
        ]

        return PedidoDetailResponse(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            estado_codigo=pedido.estado_codigo,
            cliente_email=cliente.email if cliente else None,
            cliente_nombre=cliente.nombre if cliente else None,
            cliente_apellido=cliente.apellido if cliente else None,
            direccion_calle=pedido.direccion_calle,
            direccion_numero=pedido.direccion_numero,
            direccion_piso_depto=pedido.direccion_piso_depto,
            direccion_ciudad=pedido.direccion_ciudad,
            direccion_provincia=pedido.direccion_provincia,
            direccion_codigo_postal=pedido.direccion_codigo_postal,
            direccion_pais=pedido.direccion_pais,
            direccion_referencias=pedido.direccion_referencias,
            total=pedido.total,
            costo_envio=pedido.costo_envio,
            items=items_data,
            creado_en=pedido.creado_en,
            actualizado_en=pedido.actualizado_en,
        )


# ── GET /admin/pedidos/{id}/historial/ ───────────────────────────────────

@router.get(
    "/pedidos/{pedido_id}/historial/",
    response_model=list[PedidoHistorialEntry],
    summary="Historial de estados de un pedido",
    description="Retorna el historial de transiciones de estado de un pedido.",
)
def get_pedido_historial(
    pedido_id: int,
    current_user: Any = Depends(require_role("ADMIN", "PEDIDOS")),
) -> list[PedidoHistorialEntry]:
    """GET /admin/pedidos/{id}/historial/ — historial de estados."""
    with SessionLocal() as session:
        # Verificar que existe el pedido
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        # Obtener historial
        historial_stmt = select(HistorialEstadoPedido).where(
            HistorialEstadoPedido.pedido_id == pedido_id
        ).order_by(HistorialEstadoPedido.creado_en.asc())
        historial = session.exec(historial_stmt).all()

        return [
            PedidoHistorialEntry(
                id=h.id,
                estado_anterior_codigo=h.estado_anterior_codigo,
                estado_nuevo_codigo=h.estado_nuevo_codigo,
                actor_id=h.actor_id,
                actor_tipo=h.actor_tipo if h.actor_tipo else None,
                motivo=h.motivo,
                creado_en=h.creado_en,
            )
            for h in historial
        ]
