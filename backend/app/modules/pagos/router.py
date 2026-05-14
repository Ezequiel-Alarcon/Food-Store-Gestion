"""app.modules.pagos.router

Endpoints del modulo de pagos MercadoPago.

POST   /api/v1/pagos/crear                  - crear pago (CLIENT)
POST   /api/v1/pagos/webhook                - IPN MercadoPago (publico)
GET    /api/v1/pagos/{pedido_id}            - consultar pago (auth)
POST   /api/v1/pagos/{pedido_id}/reintentar  - reintentar pago (CLIENT)
"""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from app.core.config import get_settings
from app.core.deps import get_current_user, require_role
from app.core.limiter import limiter
from app.modules.pagos.schemas import PagoCreate, PagoResponse, WebhookPayload
from app.modules.pagos.service import PagoService, _validate_webhook_signature

router = APIRouter(tags=["Pagos"])


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
@limiter.limit("60/minute")
async def webhook_mercadopago(request: Request, background_tasks: BackgroundTasks) -> dict:
    settings = get_settings()

    if settings.MP_WEBHOOK_SECRET:
        data_id = request.query_params.get("data.id", "")
        if not data_id:
            raise HTTPException(status_code=400, detail="Falta data.id en query params")

        if not _validate_webhook_signature(request, settings.MP_WEBHOOK_SECRET):
            raise HTTPException(status_code=401, detail="Firma del webhook invalida")

    try:
        body = await request.json()
    except Exception:
        body = {}
    payload = WebhookPayload(**body)

    topic = payload.topic or payload.type
    resource_id = payload.resource_id or payload.id

    if not resource_id:
        return {"status": "ignored", "reason": "Falta resource_id"}

    background_tasks.add_task(_process_webhook_task, topic, resource_id)
    return {"status": "ok"}


def _process_webhook_task(topic: str | None, resource_id: str) -> None:
    """Procesa webhook en background con su propia sesion de BD."""
    service = PagoService()
    try:
        service.procesar_webhook(topic=topic, resource_id=resource_id)
    except Exception:
        import logging
        logger = logging.getLogger(__name__)
        logger.exception(f"Error en background webhook task: topic={topic}, resource_id={resource_id}")


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
