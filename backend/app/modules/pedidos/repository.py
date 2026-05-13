"""app.modules.pedidos.repository

Repositorios para pedidos, detalles e historial de estados.
HistorialEstadoPedidoRepository es append-only (sin update/delete).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, or_
from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.auth.model import Usuario
from app.modules.pedidos.model import (
    DetallePedido,
    HistorialEstadoPedido,
    Pedido,
)


class PedidosRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def get_by_id_with_items(self, pedido_id: int) -> Pedido | None:
        return self.session.get(Pedido, pedido_id)

    def get_historial(self, pedido_id: int) -> list[HistorialEstadoPedido]:
        stmt = (
            select(HistorialEstadoPedido)
            .where(HistorialEstadoPedido.pedido_id == pedido_id)
            .order_by(HistorialEstadoPedido.creado_en.asc())
        )
        return list(self.session.exec(stmt).all())

    def list_pedidos(
        self,
        *,
        page: int,
        size: int,
        cliente_id: int | None = None,
        estado: str | None = None,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        q: str | None = None,
        order_desc: bool = True,
    ) -> list[tuple[Pedido, str]]:
        # Join para traer email sin N+1.
        stmt = select(Pedido, Usuario.email).join(Usuario, Usuario.id == Pedido.cliente_id)

        if cliente_id is not None:
            stmt = stmt.where(Pedido.cliente_id == cliente_id)
        if estado is not None:
            stmt = stmt.where(Pedido.estado_codigo == estado)
        if desde is not None:
            stmt = stmt.where(Pedido.creado_en >= desde)
        if hasta is not None:
            stmt = stmt.where(Pedido.creado_en <= hasta)

        if q:
            q_norm = q.strip()
            if q_norm:
                if q_norm.isdigit():
                    stmt = stmt.where(Pedido.id == int(q_norm))
                else:
                    like = f"%{q_norm}%"
                    stmt = stmt.where(or_(Usuario.email.ilike(like)))

        if order_desc:
            stmt = stmt.order_by(Pedido.creado_en.desc(), Pedido.id.desc())
        else:
            stmt = stmt.order_by(Pedido.creado_en.asc(), Pedido.id.asc())

        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)

        return list(self.session.exec(stmt).all())

    def count_pedidos(
        self,
        *,
        cliente_id: int | None = None,
        estado: str | None = None,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        q: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Pedido).join(Usuario, Usuario.id == Pedido.cliente_id)

        if cliente_id is not None:
            stmt = stmt.where(Pedido.cliente_id == cliente_id)
        if estado is not None:
            stmt = stmt.where(Pedido.estado_codigo == estado)
        if desde is not None:
            stmt = stmt.where(Pedido.creado_en >= desde)
        if hasta is not None:
            stmt = stmt.where(Pedido.creado_en <= hasta)

        if q:
            q_norm = q.strip()
            if q_norm:
                if q_norm.isdigit():
                    stmt = stmt.where(Pedido.id == int(q_norm))
                else:
                    like = f"%{q_norm}%"
                    stmt = stmt.where(or_(Usuario.email.ilike(like)))

        return int(self.session.exec(stmt).one())


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(session, DetallePedido)

    def get_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        stmt = select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        return list(self.session.exec(stmt).all())


class HistorialEstadoPedidoRepository(BaseRepository[HistorialEstadoPedido]):
    """Repositorio append-only. No expone update/delete (RN-DA05)."""

    def __init__(self, session: Session):
        super().__init__(session, HistorialEstadoPedido)

    def append(self, entry: HistorialEstadoPedido) -> HistorialEstadoPedido:
        self.session.add(entry)
        return entry
