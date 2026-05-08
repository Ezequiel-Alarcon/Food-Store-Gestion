"""
app.modules.ingredientes.service

Servicio para operaciones de ingredientes.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.ingredientes.model import Ingrediente
from app.modules.ingredientes.repository import IngredienteRepository
from app.modules.ingredientes.schemas import (
    IngredienteCreate,
    IngredienteUpdate,
)


class IngredienteService:
    """Servicio de ingredientes."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = IngredienteRepository(session)

    def create(self, data: IngredienteCreate) -> Ingrediente:
        """
        Crea un nuevo ingrediente.

        Args:
            data: Schema de creación

        Returns:
            Ingrediente creado

        Raises:
            HTTPException 409: Si el nombre ya existe
        """
        # Verificar nombre único
        if self.repo.exists_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un ingrediente con este nombre",
            )

        # Crear ingrediente
        ingrediente = Ingrediente(
            nombre=data.nombre,
            descripcion=data.descripcion,
            es_alergeno=data.es_alergeno,
        )

        self.repo.add(ingrediente)
        self.session.flush()
        return ingrediente

    def get_by_id(self, ingrediente_id: int) -> Ingrediente:
        """
        Obtiene un ingrediente por ID.

        Args:
            ingrediente_id: ID del ingrediente

        Returns:
            Ingrediente encontrado

        Raises:
            HTTPException 404: Si no existe o está eliminado
        """
        ingrediente = self.repo.get_active_by_id(ingrediente_id)
        if not ingrediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente no encontrado",
            )
        return ingrediente

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        es_alergeno: Optional[bool] = None,
    ) -> tuple[list[Ingrediente], int]:
        """
        Lista ingredientes con paginación y filtro opcional.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados
            es_alergeno: Filtrar por alérgenos (None = sin filtro)

        Returns:
            Tupla de (lista de ingredientes, total)
        """
        ingredientes = self.repo.list_all(skip=skip, limit=limit, es_alergeno=es_alergeno)
        total = self.repo.count_all(es_alergeno=es_alergeno)
        return ingredientes, total

    def update(self, ingrediente_id: int, data: IngredienteUpdate) -> Ingrediente:
        """
        Actualiza un ingrediente parcialmente.

        Args:
            ingrediente_id: ID del ingrediente
            data: Schema de actualización (todos los campos opcionales)

        Returns:
            Ingrediente actualizado

        Raises:
            HTTPException 404: Si no existe o está eliminado
            HTTPException 409: Si el nombre ya existe
        """
        ingrediente = self.repo.get_active_by_id(ingrediente_id)
        if not ingrediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente no encontrado",
            )

        # Verificar nombre único si se está cambiando
        if data.nombre is not None and data.nombre != ingrediente.nombre:
            if self.repo.exists_by_nombre(data.nombre, exclude_id=ingrediente_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe un ingrediente con este nombre",
                )
            ingrediente.nombre = data.nombre

        # Aplicar campos opcionales
        if data.descripcion is not None:
            ingrediente.descripcion = data.descripcion

        if data.es_alergeno is not None:
            ingrediente.es_alergeno = data.es_alergeno

        # Actualizar timestamp
        ingrediente.actualizado_en = datetime.now(timezone.utc)

        self.session.add(ingrediente)
        self.session.flush()
        return ingrediente

    def soft_delete(self, ingrediente_id: int) -> None:
        """
        Realiza soft-delete de un ingrediente.

        Args:
            ingrediente_id: ID del ingrediente

        Raises:
            HTTPException 404: Si no existe
        """
        ingrediente = self.repo.get_active_by_id(ingrediente_id)
        if not ingrediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente no encontrado",
            )

        self.repo.soft_delete(ingrediente_id)