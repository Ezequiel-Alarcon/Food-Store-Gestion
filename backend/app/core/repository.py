"""app.core.repository

BaseRepository[T] para centralizar operaciones comunes.

Se espera que los repos por feature hereden de BaseRepository y agreguen
métodos específicos sin cambiar el contrato base.
"""

from __future__ import annotations

from typing import Generic, Optional, Type, TypeVar

from sqlmodel import Session, select

TModel = TypeVar("TModel")


class BaseRepository(Generic[TModel]):
    """Repositorio genérico para entidades SQLModel."""

    def __init__(self, session: Session, model_type: Type[TModel]):
        self.session = session
        self.model_type = model_type

    def get_by_id(self, entity_id: object) -> Optional[TModel]:
        return self.session.get(self.model_type, entity_id)

    def list(self, *, offset: int = 0, limit: int = 100) -> list[TModel]:
        stmt = select(self.model_type).offset(offset).limit(limit)
        return list(self.session.exec(stmt).all())

    def add(self, entity: TModel) -> TModel:
        self.session.add(entity)
        return entity

    def delete(self, entity: TModel) -> None:
        self.session.delete(entity)
