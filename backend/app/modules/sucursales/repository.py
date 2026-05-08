"""app.modules.sucursales.repository"""

from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.sucursales.model import Sucursal


class SucursalRepository(BaseRepository[Sucursal]):
    def __init__(self, session: Session):
        super().__init__(session, Sucursal)

    def get_by_id_active(self, sucursal_id: int) -> Optional[Sucursal]:
        stmt = select(Sucursal).where(Sucursal.id == sucursal_id, Sucursal.activa == True)
        return self.session.exec(stmt).first()

    def get_all_active(self) -> list[Sucursal]:
        stmt = select(Sucursal).where(Sucursal.activa == True).order_by(Sucursal.nombre)
        return list(self.session.exec(stmt).all())
