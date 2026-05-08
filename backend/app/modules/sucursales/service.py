"""app.modules.sucursales.service

Servicio minimo para sucursales.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.sucursales.model import Sucursal
from app.modules.sucursales.repository import SucursalRepository
from app.modules.sucursales.schemas import SucursalCreate, SucursalUpdate


class SucursalesService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = SucursalRepository(session)

    def list_active(self) -> list[Sucursal]:
        return self.repo.get_all_active()

    def create(self, data: SucursalCreate) -> Sucursal:
        suc = Sucursal(
            nombre=data.nombre,
            activa=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.repo.add(suc)
        self.session.flush()
        return suc

    def update(self, sucursal_id: int, data: SucursalUpdate) -> Sucursal:
        suc = self.repo.get_by_id(sucursal_id)
        if not suc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")
        if data.nombre is not None:
            suc.nombre = data.nombre
        if data.activa is not None:
            suc.activa = data.activa
        suc.updated_at = datetime.utcnow()
        self.session.add(suc)
        self.session.flush()
        return suc
