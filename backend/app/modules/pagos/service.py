"""app.modules.pagos.service

Servicios para integracion MercadoPago: crear pago, webhook IPN, consulta, reintento.

Flujo: Router -> Service -> UnitOfWork -> Repository -> Model
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Optional

import mercadopago
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
        return str(current_user.rol)
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
                    "payer": {"id": str(cliente_id)},
                    "external_reference": external_reference,
                }
                if settings.MP_NOTIFICATION_URL:
                    payment_data["notification_url"] = settings.MP_NOTIFICATION_URL

                request_options = mercadopago.config.RequestOptions(
                    custom_headers={"x-idempotency-key": idempotency_key}
                )
                payment = sdk.payment().create(payment_data, request_options)
                mp_response = payment.get("response", {})

                pago = Pago(
                    pedido_id=data.pedido_id,
                    mp_payment_id=mp_response.get("id"),
                    idempotency_key=idempotency_key,
                    external_reference=external_reference,
                    status=mp_response.get("status", "pending"),
                    status_detail=mp_response.get("status_detail"),
                    payment_method_id=mp_response.get("payment_method_id"),
                    transaction_amount=float(monto),
                )
                session.add(pago)
                session.flush()
                return _build_pago_response(pago)
            except Exception as e:
                logger.error(f"Error al crear pago en MercadoPago: {e}")
                raise ValidationError(f"Error al procesar el pago: {str(e)}")

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
            pago.actualizado_en = datetime.utcnow()
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
        pedido.actualizado_en = datetime.utcnow()
        session.add(pedido)

        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_anterior_codigo=estado_anterior,
            estado_nuevo_codigo="CONFIRMADO",
            actor_id=None,
            actor_tipo=ActorTipo.SISTEMA.value,
            motivo="Pago aprobado por MercadoPago",
            creado_en=datetime.utcnow(),
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
                    "payer": {"id": str(cliente_id)},
                    "external_reference": external_reference,
                }
                if settings.MP_NOTIFICATION_URL:
                    payment_data["notification_url"] = settings.MP_NOTIFICATION_URL

                request_options = mercadopago.config.RequestOptions(
                    custom_headers={"x-idempotency-key": idempotency_key}
                )
                payment = sdk.payment().create(payment_data, request_options)
                mp_response = payment.get("response", {})

                pago = Pago(
                    pedido_id=pedido_id,
                    mp_payment_id=mp_response.get("id"),
                    idempotency_key=idempotency_key,
                    external_reference=external_reference,
                    status=mp_response.get("status", "pending"),
                    status_detail=mp_response.get("status_detail"),
                    payment_method_id=mp_response.get("payment_method_id"),
                    transaction_amount=float(monto),
                )
                session.add(pago)
                session.flush()
                return _build_pago_response(pago)
            except Exception as e:
                logger.error(f"Error al reintentar pago en MercadoPago: {e}")
                raise ValidationError(f"Error al procesar el reintento: {str(e)}")
