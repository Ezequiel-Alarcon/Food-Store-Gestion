"""app.modules.direcciones.service

Servicios para direcciones (usuarios y sucursales).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.database import SessionLocal
from app.core.uow import UnitOfWork
from app.modules.direcciones.model import BranchAddress, UserAddress
from app.modules.direcciones.repository import BranchAddressRepository, UserAddressRepository
from app.modules.direcciones.schemas import (
    BranchAddressCreate,
    BranchAddressUpdate,
    UserAddressCreate,
    UserAddressUpdate,
)
from app.modules.sucursales.repository import SucursalRepository


def _principal_user_id(current_user: Any) -> int:
    # current_user puede ser Usuario (modelo) o dict payload.
    if hasattr(current_user, "id"):
        return int(getattr(current_user, "id"))
    if isinstance(current_user, dict):
        sub = current_user.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return int(sub)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


class UserAddressesService:
    def __init__(self, uow: UnitOfWork | None = None):
        self.uow = uow or UnitOfWork(SessionLocal)

    def list_active(self, *, current_user: Any) -> list[UserAddress]:
        user_id = _principal_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            repo = UserAddressRepository(uow.session)
            return repo.list_active_by_user(user_id)

    def create(self, *, current_user: Any, data: UserAddressCreate) -> UserAddress:
        user_id = _principal_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            repo = UserAddressRepository(uow.session)
            addr = UserAddress(
                user_id=user_id,
                etiqueta=data.etiqueta,
                calle=data.calle,
                numero=data.numero,
                piso_depto=data.piso_depto,
                ciudad=data.ciudad,
                provincia=data.provincia,
                codigo_postal=data.codigo_postal,
                pais=data.pais,
                referencias=data.referencias,
                is_default=False,
                activa=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            repo.add(addr)
            uow.session.flush()
            return addr

    def update(self, *, current_user: Any, address_id: int, data: UserAddressUpdate) -> UserAddress:
        user_id = _principal_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            repo = UserAddressRepository(uow.session)
            addr = repo.get_by_id(address_id)
            if not addr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
            if addr.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
            if not addr.activa:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La dirección no está activa")

            # patch semantics
            for field in (
                "etiqueta",
                "calle",
                "numero",
                "piso_depto",
                "ciudad",
                "provincia",
                "codigo_postal",
                "pais",
                "referencias",
            ):
                value = getattr(data, field)
                if value is not None:
                    setattr(addr, field, value)
            addr.updated_at = datetime.now(timezone.utc)
            uow.session.add(addr)
            uow.session.flush()
            return addr

    def soft_delete(self, *, current_user: Any, address_id: int) -> None:
        user_id = _principal_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            repo = UserAddressRepository(uow.session)
            addr = repo.get_by_id(address_id)
            if not addr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
            if addr.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
            addr.activa = False
            addr.is_default = False
            addr.updated_at = datetime.now(timezone.utc)
            uow.session.add(addr)
            uow.session.flush()
            return None

    def set_default(self, *, current_user: Any, address_id: int) -> UserAddress:
        user_id = _principal_user_id(current_user)
        with self.uow as uow:
            assert uow.session is not None
            repo = UserAddressRepository(uow.session)
            addr = repo.get_by_id(address_id)
            if not addr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
            if addr.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
            if not addr.activa:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La dirección no está activa")

            # atomic: unset others then set this
            repo.unset_default_for_user(user_id)
            addr.is_default = True
            addr.updated_at = datetime.now(timezone.utc)
            uow.session.add(addr)
            uow.session.flush()
            return addr


class BranchAddressesService:
    def __init__(self, uow: UnitOfWork | None = None):
        self.uow = uow or UnitOfWork(SessionLocal)

    def list_active(self) -> list[BranchAddress]:
        with self.uow as uow:
            assert uow.session is not None
            repo = BranchAddressRepository(uow.session)
            return repo.list_active()

    def create_or_replace(self, *, branch_id: int, data: BranchAddressCreate) -> BranchAddress:
        with self.uow as uow:
            assert uow.session is not None
            suc_repo = SucursalRepository(uow.session)
            if not suc_repo.get_by_id_active(branch_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")

            repo = BranchAddressRepository(uow.session)
            existing = repo.get_active_by_branch(branch_id)
            if existing is not None:
                existing.activa = False
                existing.updated_at = datetime.now(timezone.utc)
                uow.session.add(existing)

            addr = BranchAddress(
                branch_id=branch_id,
                calle=data.calle,
                numero=data.numero,
                piso_depto=data.piso_depto,
                ciudad=data.ciudad,
                provincia=data.provincia,
                codigo_postal=data.codigo_postal,
                pais=data.pais,
                referencias=data.referencias,
                activa=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            repo.add(addr)
            uow.session.flush()
            return addr

    def update(self, *, branch_id: int, data: BranchAddressUpdate) -> BranchAddress:
        with self.uow as uow:
            assert uow.session is not None
            repo = BranchAddressRepository(uow.session)
            addr = repo.get_active_by_branch(branch_id)
            if not addr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección de sucursal no encontrada")
            for field in (
                "calle",
                "numero",
                "piso_depto",
                "ciudad",
                "provincia",
                "codigo_postal",
                "pais",
                "referencias",
            ):
                value = getattr(data, field)
                if value is not None:
                    setattr(addr, field, value)
            addr.updated_at = datetime.now(timezone.utc)
            uow.session.add(addr)
            uow.session.flush()
            return addr

    def soft_delete(self, *, branch_id: int) -> None:
        with self.uow as uow:
            assert uow.session is not None
            repo = BranchAddressRepository(uow.session)
            addr = repo.get_active_by_branch(branch_id)
            if not addr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección de sucursal no encontrada")
            addr.activa = False
            addr.updated_at = datetime.now(timezone.utc)
            uow.session.add(addr)
            uow.session.flush()
            return None
