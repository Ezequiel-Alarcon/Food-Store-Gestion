"""app.modules.pagos.router

Endpoints del modulo de pagos MercadoPago.

POST   /api/v1/pagos/crear                  - crear pago (CLIENT)
POST   /api/v1/pagos/webhook                - IPN MercadoPago (publico)
GET    /api/v1/pagos/{pedido_id}            - consultar pago (auth)
POST   /api/v1/pagos/{pedido_id}/reintentar  - reintentar pago (CLIENT)
"""
from fastapi import APIRouter, Depends, Request, status
from app.core.deps import get_current_user, require_role
from app.modules.pagos.schemas import PagoCreate, PagoResponse, WebhookPayload
from app.modules.pagos.service import PagoService

router = APIRouter()


@router.post(
    "/crear",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pago",
    description="Crea una orden de pago en MercadoPago. Requiere rol CLIENT.",
)
def crear_pago(
    data: PagoCreate,
    current_user=Depends(require_role("CLIENT")),
) -> PagoResponse:
    service = PagoService()
    return service.crear_pago(data, current_user)


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook IPN MercadoPago",
    description="Endpoint publico para notificaciones IPN de MercadoPago. Responde 200 inmediatamente (RN-PA03).",
)
async def webhook_mercadopago(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        body = {}
    payload = WebhookPayload(**body)
    service = PagoService()
    service.procesar_webhook(
        topic=payload.topic or payload.type,
        resource_id=payload.resource_id or payload.id,
    )
    return {"status": "ok"}


@router.get(
    "/{pedido_id}",
    response_model=PagoResponse,
    summary="Consultar estado de pago",
    description="Retorna el estado del ultimo pago asociado al pedido. Propietario o ADMIN.",
)
def consultar_pago(
    pedido_id: int,
    current_user=Depends(get_current_user),
) -> PagoResponse:
    service = PagoService()
    return service.get_pago(pedido_id, current_user)


@router.post(
    "/{pedido_id}/reintentar",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Reintentar pago rechazado",
    description="Reintenta un pago que fue rechazado. Requiere rol CLIENT y ser propietario.",
)
def reintentar_pago(
    pedido_id: int,
    current_user=Depends(require_role("CLIENT")),
) -> PagoResponse:
    service = PagoService()
    return service.reintentar_pago(pedido_id, current_user)
