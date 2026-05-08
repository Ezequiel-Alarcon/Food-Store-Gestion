"""app.modules.direcciones.repository"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import text
from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.direcciones.model import BranchAddress, UserAddress


class UserAddressRepository(BaseRepository[UserAddress]):
    def __init__(self, session: Session):
        super().__init__(session, UserAddress)

    def list_active_by_user(self, user_id: int) -> list[UserAddress]:
        stmt = (
            select(UserAddress)
            .where(UserAddress.user_id == user_id, UserAddress.activa == True)
            .order_by(UserAddress.is_default.desc(), UserAddress.id.desc())
        )
        return list(self.session.exec(stmt).all())

    def get_active_by_id(self, address_id: int) -> Optional[UserAddress]:
        stmt = select(UserAddress).where(UserAddress.id == address_id, UserAddress.activa == True)
        return self.session.exec(stmt).first()

    def get_by_id_for_user(self, address_id: int, user_id: int) -> Optional[UserAddress]:
        stmt = select(UserAddress).where(UserAddress.id == address_id, UserAddress.user_id == user_id)
        return self.session.exec(stmt).first()

    def unset_default_for_user(self, user_id: int) -> None:
        # SQLModel bulk updates are not exposed cleanly; raw SQL is simplest.
        self.session.exec(
            text("UPDATE user_addresses SET is_default = false WHERE user_id = :user_id AND activa = true"),
            params={"user_id": user_id},
        )


class BranchAddressRepository(BaseRepository[BranchAddress]):
    def __init__(self, session: Session):
        super().__init__(session, BranchAddress)

    def list_active(self) -> list[BranchAddress]:
        stmt = select(BranchAddress).where(BranchAddress.activa == True).order_by(BranchAddress.branch_id)
        return list(self.session.exec(stmt).all())

    def get_active_by_branch(self, branch_id: int) -> Optional[BranchAddress]:
        stmt = select(BranchAddress).where(BranchAddress.branch_id == branch_id, BranchAddress.activa == True)
        return self.session.exec(stmt).first()
