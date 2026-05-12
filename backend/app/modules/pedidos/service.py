"""app.modules.pedidos.service

Servicios para pedidos: creación atómica, FSM, historial.

Flujo: Router → Service → UnitOfWork → Repository → Model
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.database import SessionLocal
from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.core.uow import UnitOfWork
from app.modules.direcciones.model import UserAddress
from app.modules.pedidos.fsm import check_cancel_permission, validate_transition
from app.modules.pedidos.model import (
    ActorTipo,
    DetallePedido,
    HistorialEstadoPedido,
    Pedido,
)
from app.modules.pedidos.repository import (
    DetallePedidoRepository,
    HistorialEstadoPedidoRepository,
    PedidosRepository,
)
from app.modules.pedidos.schemas import (
    DetallePedidoRead,
    EstadoTransicionCreate,
    HistorialEstadoRead,
    PedidoCreate,
    PedidoRead,
)
from app.modules.productos.model import Producto


def _get_rol(current_user: Any) -> str:
    if hasattr(current_user, "rol"):
        return str(current_user.rol)
    if isinstance(current_user, dict):
        return str(current_user.get("rol") or current_user.get("role") or "")
    return ""


def _get_user_id(current_user: Any) -> int:
    if hasattr(current_user, "id"):
        return int(current_user.id)
    if isinstance(current_user, dict):
        sub = current_user.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return int(sub)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def _build_pedido_read(pedido: Pedido, items: list[DetallePedido]) -> PedidoRead:
    return PedidoRead(
        id=pedido.id,  # type: ignore[arg-type]
        cliente_id=pedido.cliente_id,
        estado_codigo=pedido.estado_codigo,
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
        items=[
            DetallePedidoRead(
                id=d.id,  # type: ignore[arg-type]
                producto_id=d.producto_id,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                exclusiones=list(d.exclusiones) if d.exclusiones else [],
            )
            for d in items
        ],
        creado_en=pedido.creado_en,
        actualizado_en=pedido.actualizado_en,
    )


class PedidosService:
    def __init__(self, uow: UnitOfWork | None = None):
        self.uow = uow or UnitOfWork(SessionLocal)

    # ------------------------------------------------------------------
    # Creación atómica (RN-PE01)
    # ------------------------------------------------------------------

    def crear_pedido(self, data: PedidoCreate, current_user: Any) -> PedidoRead:
        """Crea un pedido de forma atómica con snapshots de precio y dirección."""
        cliente_id = _get_user_id(current_user)

        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session

            # (a) Validar que la dirección pertenece al cliente
            direccion = session.get(UserAddress, data.direccion_id)
            if not direccion or not direccion.activa:
                raise NotFoundError("Dirección", data.direccion_id)
            if direccion.user_id != cliente_id:
                raise ForbiddenError("La dirección no pertenece al usuario autenticado")

            # (b) SELECT FOR UPDATE del stock de cada producto + (c) validar stock
            productos_info: dict[int, Producto] = {}
            for item in data.items:
                stmt = (
                    select(Producto)
                    .where(Producto.id == item.producto_id)
                    .with_for_update()
                )
                producto = session.exec(stmt).first()
                if not producto or producto.eliminado_en is not None:
                    raise NotFoundError("Producto", item.producto_id)
                if not producto.activo:
                    raise ValidationError(f"El producto '{producto.nombre}' no está disponible")
                if producto.stock < item.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para '{producto.nombre}': "
                        f"disponible={producto.stock}, solicitado={item.cantidad}"
                    )
                productos_info[item.producto_id] = producto

            # (d) Calcular total y crear Pedido con snapshot de dirección
            subtotales = [
                productos_info[item.producto_id].precio * item.cantidad
                for item in data.items
            ]
            total = sum(subtotales)

            pedido = Pedido(
                cliente_id=cliente_id,
                estado_codigo="PENDIENTE",
                direccion_calle=direccion.calle,
                direccion_numero=direccion.numero,
                direccion_piso_depto=direccion.piso_depto,
                direccion_ciudad=direccion.ciudad,
                direccion_provincia=direccion.provincia,
                direccion_codigo_postal=direccion.codigo_postal,
                direccion_pais=direccion.pais,
                direccion_referencias=direccion.referencias,
                total=total,
                costo_envio=0.0,
                creado_en=datetime.utcnow(),
                actualizado_en=datetime.utcnow(),
            )
            session.add(pedido)
            session.flush()  # obtener pedido.id

            # (e) Insertar DetallePedido con precio snapshot
            detalles: list[DetallePedido] = []
            for item in data.items:
                producto = productos_info[item.producto_id]
                detalle = DetallePedido(
                    pedido_id=pedido.id,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=producto.precio,
                    exclusiones=item.exclusiones or [],
                )
                session.add(detalle)
                detalles.append(detalle)

            session.flush()

            # (f) Registro inicial en historial
            historial_entry = HistorialEstadoPedido(
                pedido_id=pedido.id,
                estado_anterior_codigo=None,
                estado_nuevo_codigo="PENDIENTE",
                actor_id=cliente_id,
                actor_tipo=ActorTipo.USUARIO.value,
                motivo=None,
                creado_en=datetime.utcnow(),
            )
            session.add(historial_entry)
            session.flush()

            return _build_pedido_read(pedido, detalles)

    # ------------------------------------------------------------------
    # Consulta de pedido por ID (RBAC: CLIENT solo propios)
    # ------------------------------------------------------------------

    def get_pedido(self, pedido_id: int, current_user: Any) -> PedidoRead:
        user_id = _get_user_id(current_user)
        rol = _get_rol(current_user)

        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session

            repo = PedidosRepository(session)
            pedido = repo.get_by_id_with_items(pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", pedido_id)

            if rol not in ("ADMIN", "PEDIDOS") and pedido.cliente_id != user_id:
                raise ForbiddenError("No tenés acceso a este pedido")

            detalle_repo = DetallePedidoRepository(session)
            items = detalle_repo.get_by_pedido(pedido_id)

            return _build_pedido_read(pedido, items)

    # ------------------------------------------------------------------
    # FSM: transicionar estado
    # ------------------------------------------------------------------

    def transicionar_estado(
        self,
        pedido_id: int,
        data: EstadoTransicionCreate,
        current_user: Any,
    ) -> PedidoRead:
        user_id = _get_user_id(current_user)
        rol = _get_rol(current_user)

        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session

            repo = PedidosRepository(session)
            pedido = repo.get_by_id_with_items(pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", pedido_id)

            # CLIENT solo puede operar sobre sus propios pedidos
            if rol == "CLIENT" and pedido.cliente_id != user_id:
                raise ForbiddenError("No tenés acceso a este pedido")

            estado_actual = pedido.estado_codigo
            estado_destino = data.nuevo_estado

            # (a) Validar FSM
            validate_transition(estado_actual, estado_destino)

            # (b) Si es CANCELADO: verificar permisos de rol
            if estado_destino == "CANCELADO":
                check_cancel_permission(estado_actual, rol)

                # Restaurar stock si venía de CONFIRMADO (RN-FS05)
                if estado_actual == "CONFIRMADO":
                    detalle_repo = DetallePedidoRepository(session)
                    items = detalle_repo.get_by_pedido(pedido_id)
                    for item in items:
                        stmt = (
                            select(Producto)
                            .where(Producto.id == item.producto_id)
                            .with_for_update()
                        )
                        producto = session.exec(stmt).first()
                        if producto:
                            producto.stock += item.cantidad
                            session.add(producto)

            # (c) Actualizar estado del pedido
            pedido.estado_codigo = estado_destino
            pedido.actualizado_en = datetime.utcnow()
            session.add(pedido)

            # (d) Registrar en historial
            historial_entry = HistorialEstadoPedido(
                pedido_id=pedido.id,
                estado_anterior_codigo=estado_actual,
                estado_nuevo_codigo=estado_destino,
                actor_id=user_id,
                actor_tipo=ActorTipo.USUARIO.value,
                motivo=data.motivo,
                creado_en=datetime.utcnow(),
            )
            session.add(historial_entry)
            session.flush()

            detalle_repo = DetallePedidoRepository(session)
            items = detalle_repo.get_by_pedido(pedido_id)
            return _build_pedido_read(pedido, items)

    # ------------------------------------------------------------------
    # Historial de estados (RBAC: CLIENT solo propios)
    # ------------------------------------------------------------------

    def get_historial(self, pedido_id: int, current_user: Any) -> list[HistorialEstadoRead]:
        user_id = _get_user_id(current_user)
        rol = _get_rol(current_user)

        with self.uow as uow:
            assert uow.session is not None
            session: Session = uow.session

            repo = PedidosRepository(session)
            pedido = repo.get_by_id_with_items(pedido_id)
            if not pedido:
                raise NotFoundError("Pedido", pedido_id)

            if rol not in ("ADMIN", "PEDIDOS") and pedido.cliente_id != user_id:
                raise ForbiddenError("No tenés acceso al historial de este pedido")

            historial = repo.get_historial(pedido_id)
            return [
                HistorialEstadoRead(
                    id=h.id,  # type: ignore[arg-type]
                    estado_anterior_codigo=h.estado_anterior_codigo,
                    estado_nuevo_codigo=h.estado_nuevo_codigo,
                    actor_id=h.actor_id,
                    actor_tipo=h.actor_tipo,
                    motivo=h.motivo,
                    creado_en=h.creado_en,
                )
                for h in historial
            ]
