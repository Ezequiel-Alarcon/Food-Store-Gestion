"""Service de ejemplo.

Demuestra el uso de UnitOfWork:
- caso OK: el UoW comitea
- caso error: el UoW hace rollback
"""

from __future__ import annotations

from sqlmodel import Session

from app.core.uow import UnitOfWork
from app.modules.patterns_example.model import ExampleItem
from app.modules.patterns_example.repository import ExampleItemRepository


class ExampleService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_item_and_commit(self, name: str) -> ExampleItem:
        with self.uow as uow:
            assert uow.session is not None
            repo = ExampleItemRepository(uow.session)
            item = ExampleItem(name=name)
            repo.add(item)
            # flush para que quede disponible el ID antes del commit
            uow.session.flush()
            return item

    def create_item_and_fail(self, name: str) -> None:
        with self.uow as uow:
            assert uow.session is not None
            repo = ExampleItemRepository(uow.session)
            repo.add(ExampleItem(name=name))
            # Simulamos un error de negocio; el UoW debe hacer rollback.
            raise RuntimeError("forzar rollback")
