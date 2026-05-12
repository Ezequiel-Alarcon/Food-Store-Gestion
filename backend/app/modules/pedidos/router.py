"""app.modules.pedidos.router

Endpoints del módulo de pedidos.

POST   /api/v1/pedidos                  — crear pedido (CLIENT)
GET    /api/v1/pedidos/{id}             — detalle de pedido (auth)
PATCH  /api/v1/pedidos/{id}/estado      — transición FSM (PEDIDOS/ADMIN)
GET    /api/v1/pedidos/{id}/historial   — historial de estados (auth)
"""
from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_user, require_role
from app.modules.pedidos.schemas import (
    EstadoTransicionCreate,
    HistorialEstadoRead,
    PedidoCreate,
    PedidoRead,
)
from app.modules.pedidos.service import PedidosService

router = APIRouter()


@router.post(
    "/",
    response_model=PedidoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pedido",
    description="Crea un pedido desde el carrito del cliente. Requiere rol CLIENT.",
)
def crear_pedido(
    data: PedidoCreate,
    current_user=Depends(require_role("CLIENT")),
) -> PedidoRead:
    service = PedidosService()
    return service.crear_pedido(data, current_user)


@router.get(
    "/{pedido_id}",
    response_model=PedidoRead,
    summary="Detalle de pedido",
    description="Retorna el detalle de un pedido. CLIENT solo puede ver sus propios pedidos.",
)
def get_pedido(
    pedido_id: int,
    current_user=Depends(get_current_user),
) -> PedidoRead:
    service = PedidosService()
    return service.get_pedido(pedido_id, current_user)


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoRead,
    summary="Transicionar estado del pedido",
    description=(
        "Avanza el estado del pedido según la FSM. "
        "RBAC granular en el servicio: CLIENT solo puede cancelar pedidos propios en PENDIENTE. "
        "El motivo es obligatorio al cancelar."
    ),
)
def transicionar_estado(
    pedido_id: int,
    data: EstadoTransicionCreate,
    current_user=Depends(get_current_user),
) -> PedidoRead:
    service = PedidosService()
    return service.transicionar_estado(pedido_id, data, current_user)


@router.get(
    "/{pedido_id}/historial",
    response_model=list[HistorialEstadoRead],
    summary="Historial de estados del pedido",
    description="Retorna el historial de transiciones en orden cronológico.",
)
def get_historial(
    pedido_id: int,
    current_user=Depends(get_current_user),
) -> list[HistorialEstadoRead]:
    service = PedidosService()
    return service.get_historial(pedido_id, current_user)
