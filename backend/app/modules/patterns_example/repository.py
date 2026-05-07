"""Repositorio de ejemplo.

Ejemplo de extensión de BaseRepository para un modelo concreto.
"""

from __future__ import annotations

from sqlmodel import Session

from app.core.repository import BaseRepository
from app.modules.patterns_example.model import ExampleItem


class ExampleItemRepository(BaseRepository[ExampleItem]):
    def __init__(self, session: Session):
        super().__init__(session=session, model_type=ExampleItem)
