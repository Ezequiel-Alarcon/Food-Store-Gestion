"""
app.modules.ingredientes.repository

Repository para operaciones de ingredientes.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.ingredientes.model import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):
    """
    Repository para operaciones de ingredientes.

    Hereda de BaseRepository y agrega métodos específicos del dominio.
    """

    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def get_by_nombre(self, nombre: str) -> Optional[Ingrediente]:
        """Busca un ingrediente por nombre, excluyendo eliminados."""
        stmt = select(Ingrediente).where(
            Ingrediente.nombre == nombre,
            Ingrediente.eliminado_en == None,
        )
        return self.session.exec(stmt).first()

    def get_active_by_id(self, entity_id: int) -> Optional[Ingrediente]:
        """Obtiene ingrediente solo si no está eliminado."""
        stmt = select(Ingrediente).where(
            Ingrediente.id == entity_id,
            Ingrediente.eliminado_en == None,
        )
        return self.session.exec(stmt).first()

    def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
        es_alergeno: Optional[bool] = None,
    ) -> list[Ingrediente]:
        """
        Lista ingredientes activos con paginación y filtro opcional.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados (default 20)
            es_alergeno: Filtrar por alérgenos (None = sin filtro)

        Returns:
            Lista de ingredientes
        """
        stmt = select(Ingrediente).where(Ingrediente.eliminado_en == None)

        if es_alergeno is not None:
            stmt = stmt.where(Ingrediente.es_alergeno == es_alergeno)

        stmt = stmt.order_by(Ingrediente.nombre).offset(skip).limit(limit)
        return list(self.session.exec(stmt).all())

    def count_all(self, es_alergeno: Optional[bool] = None) -> int:
        """
        Cuenta ingredientes activos con filtro opcional.

        Args:
            es_alergeno: Filtrar por alérgenos (None = sin filtro)

        Returns:
            Total de ingredientes
        """
        stmt = select(Ingrediente).where(Ingrediente.eliminado_en == None)

        if es_alergeno is not None:
            stmt = stmt.where(Ingrediente.es_alergeno == es_alergeno)

        return len(list(self.session.exec(stmt).all()))

    def soft_delete(self, entity_id: int) -> Optional[Ingrediente]:
        """
        Realiza soft-delete de un ingrediente.

        Args:
            entity_id: ID del ingrediente

        Returns:
            Ingrediente marcado como eliminado o None si no existe
        """
        ingrediente = self.get_active_by_id(entity_id)
        if ingrediente:
            ingrediente.eliminado_en = datetime.now(timezone.utc)
            self.session.add(ingrediente)
            self.session.flush()
        return ingrediente

    def exists_by_nombre(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un ingrediente con el mismo nombre (excluyendo eliminados).

        Args:
            nombre: Nombre a verificar
            exclude_id: ID a excluir (para operaciones de update)

        Returns:
            True si existe, False si no
        """
        stmt = select(Ingrediente).where(
            Ingrediente.nombre == nombre,
            Ingrediente.eliminado_en == None,
        )

        if exclude_id is not None:
            stmt = stmt.where(Ingrediente.id != exclude_id)

        return self.session.exec(stmt).first() is not None