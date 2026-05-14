"""app.modules.pagos.service

Servicios para integracion MercadoPago: crear pago, webhook IPN, consulta, reintento.

Flujo: Router -> Service -> UnitOfWork -> Repository -> Model
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import mercadopago
import requests
from fastapi import Request
from sqlmodel import Session, select

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.core.uow import UnitOfWork
from app.modules.pagos.model import Pago
from app.modules.pagos.repository import PagoRepository
from app.modules.pagos.schemas import PagoCreate, PagoResponse
from app.modules.pedidos.model import ActorTipo, HistorialEstadoPedido, Pedido
from app.modules.pedidos.repository import DetallePedidoRepository
from app.modules.productos.model import Producto

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_rol(current_user: Any) -> str:
    if hasattr(current_user, "rol"):
        rol = current_user.rol
        return rol.value if hasattr(rol, "value") else str(rol)
    if isinstance(current_user, dict):
        return str(current_user.get("rol") or current_user.get("role") or "")
    return ""


def _get_user_id(current_user: Any) -> int:
    import fastapi
    if hasattr(current_user, "id"):
        return int(current_user.id)
    if isinstance(current_user, dict):
        sub = current_user.get("sub")
        if sub is None:
            raise fastapi.HTTPException(status_code=401, detail="Token invalido")
        return int(sub)
    raise fastapi.HTTPException(status_code=401, detail="Token invalido")


def _generar_external_reference(pedido_id: int) -> str:
    short_uuid = uuid.uuid4().hex[:8]
    return f"pedido-{pedido_id}-{short_uuid}"


def _validate_webhook_signature(request: Request, secret: str) -> bool:
    """Valida la firma HMAC SHA256 del webhook de MercadoPago.

    Implementa el algoritmo documentado por MP:
    1. Extraer ts y v1 del header x-signature
    2. Construir manifest: id:{data.id};request-id:{x-request-id};ts:{ts};
    3. HMAC SHA256(secret, manifest) == v1

    Retorna True si la firma es válida o si secret está vacío (modo dev).
    Retorna False si la firma es inválida.
    """
    if not secret:
        return True

    x_signature = request.headers.get("x-signature", "")
    if not x_signature:
        return False

    parts = dict(part.split("=", 1) for part in x_signature.split(",") if "=" in part)
    ts = parts.get("ts", "")
    v1 = parts.get("v1", "")
    if not ts or not v1:
        return False

    data_id = request.query_params.get("data.id", "")
    if not data_id:
        return False

    x_request_id = request.headers.get("x-request-id", "")

    manifest = f"id:{data_id.lower()};request-id:{x_request_id};ts:{ts};"
    computed = hmac.new(
        secret.encode(), manifest.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed, v1)


def _handle_mp_error(e: Exception, operation: str) -> None:
    """Clasifica errores de MercadoPago y lanza excepciones HTTP apropiadas."""
    from fastapi import HTTPException

    logger.error(f"Error en {operation}: {e}")

    if isinstance(e, requests.exceptions.Timeout):
        raise HTTPException(
            status_code=504,
            detail="El proveedor de pagos no responde. Intente nuevamente.",
        )
    if isinstance(e, requests.exceptions.ConnectionError):
        raise HTTPException(
            status_code=502,
            detail="Error de conexion con el proveedor de pagos.",
        )

    # MercadoPago API errors via SDK (status code in response)
    status_code = getattr(e, "status", None) or getattr(e, "status_code", None)
    if status_code == 401:
        raise HTTPException(
            status_code=502,
            detail="Error de autenticacion con el proveedor de pagos.",
        )
    if status_code == 429:
        raise HTTPException(
            status_code=503,
            detail="Proveedor de pagos momentaneamente no disponible. Reintente en unos segundos.",
        )

    raise ValidationError(f"Error al procesar {operation}: {str(e)}")


def _build_payer_data(current_user: Any, cliente_id: int) -> dict:
    """Construye el objeto payer con datos completos para mejorar tasa de aprobacion."""
    payer: dict = {
        "email": getattr(current_user, "email", ""),
        "first_name": getattr(current_user, "nombre", ""),
    }
    apellido = getattr(current_user, "apellido", "")
    if apellido:
        payer["last_name"] = apellido

    telefono = getattr(current_user, "telefono", None)
    if telefono:
        payer["phone"] = {"number": telefono}

    return payer


def _build_pago_response(pago: Pago) -> PagoResponse:
    return PagoResponse(
        id=pago.id,
        pedido_id=pago.pedido_id,
        mp_payment_id=pago.mp_payment_id,
        idempotency_key=pago.idempotency_key,
        external_reference=pago.external_reference,
        status=pago.status,
        status_detail=pago.status_detail,
        payment_method_id=pago.payment_method_id,
        transaction_amount=pago.transaction_amount,
        creado_en=pago.creado_en,
        actualizado_en=pago.actualizado_en,
    )


class PagoService:
    def __init__(self, uow: UnitOfWork | None = None):
        self.uow = uow or UnitOfWork(SessionLocal)

    def crear_pago(self, data: PagoCreate, current_user: Any) -> PagoResponse:
        cliente_id = _get_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session
            pedido = session.get(Pedido, data.pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", data.pedido_id)
            if pedido.cliente_id != cliente_id:
                raise ForbiddenError("No tenes acceso a este pedido")
            if pedido.estado_codigo != "PENDIENTE":
                raise ValidationError("Solo pedidos en estado PENDIENTE pueden iniciar pago")

            monto = pedido.total
            idempotency_key = str(uuid.uuid4())
            external_reference = _generar_external_reference(data.pedido_id)

            try:
                sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
                payment_data = {
                    "transaction_amount": float(monto),
                    "description": f"Pedido #{data.pedido_id} - Food Store",
                    "payment_method_id": data.payment_method_id,
                    "payer": _build_payer_data(current_user, cliente_id),
                    "external_reference": external_reference,
                }
                if settings.MP_NOTIFICATION_URL:
                    payment_data["notification_url"] = settings.MP_NOTIFICATION_URL
                if data.token:
                    payment_data["token"] = data.token

                request_options = mercadopago.config.RequestOptions(
                    custom_headers={"x-idempotency-key": idempotency_key}
                )
                payment = sdk.payment().create(payment_data, request_options)
                mp_status = payment.get("status", 500)
                mp_response = payment.get("response", {})

                if mp_status >= 400:
                    error_msg = mp_response.get("message", str(mp_response))
                    logger.error(f"MP API error {mp_status}: {error_msg}")
                    raise ValidationError(f"MercadoPago rechazo la solicitud ({mp_status}): {error_msg}")

                pago = Pago(
                    pedido_id=data.pedido_id,
                    mp_payment_id=mp_response.get("id"),
                    idempotency_key=idempotency_key,
                    external_reference=external_reference,
                    status=str(mp_response.get("status", "pending")),
                    status_detail=mp_response.get("status_detail"),
                    payment_method_id=mp_response.get("payment_method_id"),
                    transaction_amount=float(monto),
                )
                session.add(pago)
                session.flush()
                return _build_pago_response(pago)
            except Exception as e:
                _handle_mp_error(e, "crear pago")

    def procesar_webhook(self, topic: str | None, resource_id: str | None) -> dict:
        if topic != "payment" and resource_id is None:
            return {"status": "ignored", "reason": f"topic '{topic}' no es 'payment'"}

        try:
            mp_payment_id = int(resource_id)
        except (TypeError, ValueError):
            return {"status": "ignored", "reason": f"resource_id invalido: {resource_id}"}

        estado_mp = self._consultar_estado_mp(mp_payment_id)
        if not estado_mp:
            return {"status": "error", "reason": "No se pudo consultar el estado a MP"}

        status = estado_mp.get("status", "")
        status_detail = estado_mp.get("status_detail", "")

        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session
            repo = PagoRepository(session)
            pago = repo.find_by_mp_payment_id(mp_payment_id)
            if not pago:
                return {"status": "ignored", "reason": "Pago no encontrado en BD"}
            if pago.status == status:
                return {"status": "already_processed", "payment_status": status}

            pago.status = status
            pago.status_detail = status_detail
            pago.actualizado_en = datetime.now(timezone.utc)
            session.add(pago)

            if status == "approved":
                self._confirmar_pedido_en_sesion(session, pago)

            session.flush()
            return {"status": "processed", "payment_status": status}

    def _consultar_estado_mp(self, mp_payment_id: int) -> dict | None:
        try:
            sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
            result = sdk.payment().get(mp_payment_id)
            response = result.get("response", {})
            return response if response else None
        except requests.exceptions.Timeout:
            logger.error(f"Timeout consultando MP API para payment {mp_payment_id}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexion al consultar MP API para payment {mp_payment_id}")
            return None
        except Exception as e:
            logger.error(f"Error consultando MP API para payment {mp_payment_id}: {e}")
            return None

    def _confirmar_pedido_en_sesion(self, session: Session, pago: Pago) -> None:
        pedido = session.get(Pedido, pago.pedido_id)
        if not pedido or pedido.estado_codigo != "PENDIENTE":
            return

        detalle_repo = DetallePedidoRepository(session)
        items = detalle_repo.get_by_pedido(pago.pedido_id)

        for item in items:
            stmt = select(Producto).where(Producto.id == item.producto_id).with_for_update()
            producto = session.exec(stmt).first()
            if not producto:
                raise ValidationError(f"Producto {item.producto_id} no encontrado al confirmar pago")
            if producto.stock < item.cantidad:
                raise ValidationError(
                    f"Stock insuficiente para '{producto.nombre}': disponible={producto.stock}, necesario={item.cantidad}"
                )
            producto.stock -= item.cantidad
            session.add(producto)

        estado_anterior = pedido.estado_codigo
        pedido.estado_codigo = "CONFIRMADO"
        pedido.actualizado_en = datetime.now(timezone.utc)
        session.add(pedido)

        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_anterior_codigo=estado_anterior,
            estado_nuevo_codigo="CONFIRMADO",
            actor_id=None,
            actor_tipo=ActorTipo.SISTEMA.value,
            motivo="Pago aprobado por MercadoPago",
            creado_en=datetime.now(timezone.utc),
        )
        session.add(historial)
        logger.info(f"Pedido {pago.pedido_id} confirmado por pago {pago.mp_payment_id}")

    def get_pago(self, pedido_id: int, current_user: Any) -> PagoResponse:
        user_id = _get_user_id(current_user)
        rol = _get_rol(current_user)
        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session
            pedido = session.get(Pedido, pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", pedido_id)
            if rol not in ("ADMIN", "PEDIDOS") and pedido.cliente_id != user_id:
                raise ForbiddenError("No tenes acceso al pago de este pedido")
            repo = PagoRepository(session)
            pago = repo.find_latest_by_pedido_id(pedido_id)
            if not pago:
                raise NotFoundError("Pago", f"pedido {pedido_id}")
            return _build_pago_response(pago)

    def reintentar_pago(self, pedido_id: int, current_user: Any) -> PagoResponse:
        cliente_id = _get_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session
            pedido = session.get(Pedido, pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", pedido_id)
            if pedido.cliente_id != cliente_id:
                raise ForbiddenError("No tenes acceso a este pedido")
            if pedido.estado_codigo != "PENDIENTE":
                raise ValidationError("Solo pedidos en PENDIENTE pueden reintentar pago")

            repo = PagoRepository(session)
            ultimo_pago = repo.find_latest_by_pedido_id(pedido_id)
            if not ultimo_pago:
                raise ValidationError("No hay pagos previos para reintentar")
            if ultimo_pago.status == "approved":
                raise ValidationError("El pago ya fue aprobado")
            if ultimo_pago.status in ("pending", "in_process"):
                raise ValidationError("El pago aun esta en proceso, no se puede reintentar")

            idempotency_key = str(uuid.uuid4())
            external_reference = _generar_external_reference(pedido_id)
            monto = pedido.total

            try:
                sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
                payment_data = {
                    "transaction_amount": float(monto),
                    "description": f"Pedido #{pedido_id} - Food Store (reintento)",
                    "payer": _build_payer_data(current_user, cliente_id),
                    "external_reference": external_reference,
                }
                if settings.MP_NOTIFICATION_URL:
                    payment_data["notification_url"] = settings.MP_NOTIFICATION_URL

                request_options = mercadopago.config.RequestOptions(
                    custom_headers={"x-idempotency-key": idempotency_key}
                )
                payment = sdk.payment().create(payment_data, request_options)
                mp_status = payment.get("status", 500)
                mp_response = payment.get("response", {})

                if mp_status >= 400:
                    error_msg = mp_response.get("message", str(mp_response))
                    logger.error(f"MP API error {mp_status}: {error_msg}")
                    raise ValidationError(f"MercadoPago rechazo el reintento ({mp_status}): {error_msg}")

                pago = Pago(
                    pedido_id=pedido_id,
                    mp_payment_id=mp_response.get("id"),
                    idempotency_key=idempotency_key,
                    external_reference=external_reference,
                    status=str(mp_response.get("status", "pending")),
                    status_detail=mp_response.get("status_detail"),
                    payment_method_id=mp_response.get("payment_method_id"),
                    transaction_amount=float(monto),
                )
                session.add(pago)
                session.flush()
                return _build_pago_response(pago)
            except Exception as e:
                _handle_mp_error(e, "reintentar pago")
