"""app.modules.pagos.repository

Repositorio para la entidad Pago.
"""
from __future__ import annotations
from typing import Optional, Sequence
from sqlmodel import select
from app.core.repository import BaseRepository
from app.modules.pagos.model import Pago


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session):
        super().__init__(session, Pago)

    def find_by_pedido_id(self, pedido_id: int) -> Sequence[Pago]:
        stmt = select(Pago).where(Pago.pedido_id == pedido_id).order_by(Pago.creado_en.desc())
        return self.session.exec(stmt).all()

    def find_by_idempotency_key(self, key: str) -> Optional[Pago]:
        stmt = select(Pago).where(Pago.idempotency_key == key)
        return self.session.exec(stmt).first()

    def find_by_mp_payment_id(self, mp_payment_id: int) -> Optional[Pago]:
        stmt = select(Pago).where(Pago.mp_payment_id == mp_payment_id)
        return self.session.exec(stmt).first()

    def find_latest_by_pedido_id(self, pedido_id: int) -> Optional[Pago]:
        stmt = select(Pago).where(Pago.pedido_id == pedido_id).order_by(Pago.creado_en.desc()).limit(1)
        return self.session.exec(stmt).first()
