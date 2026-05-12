"""app.modules.pedidos.repository

Repositorios para pedidos, detalles e historial de estados.
HistorialEstadoPedidoRepository es append-only (sin update/delete).
"""
from __future__ import annotations

from sqlmodel import Session, select

from app.core.repository import BaseRepository
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
