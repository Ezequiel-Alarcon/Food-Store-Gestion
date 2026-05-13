"""
app.modules.categorias.service

Servicio para operaciones de categorías.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.categorias.model import Categoria
from app.modules.categorias.repository import CategoriaRepository
from app.modules.categorias.schemas import (
    CategoriaCreate,
    CategoriaTreeResponse,
    CategoriaUpdate,
)


def _generate_slug(nombre: str) -> str:
    """Genera un slug a partir del nombre."""
    # Convertir a minúsculas
    slug = nombre.lower()
    # Reemplazar espacios con guiones
    slug = re.sub(r'\s+', '-', slug)
    # Eliminar caracteres especiales (mantener solo letras, números y guiones)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Eliminar guiones duplicados
    slug = re.sub(r'-+', '-', slug)
    # Eliminar guiones al inicio y final
    slug = slug.strip('-')
    return slug


def _ensure_unique_slug(repo: CategoriaRepository, base_slug: str, exclude_id: Optional[int] = None) -> str:
    """Asegura que el slug sea único, agregando sufijos si es necesario."""
    slug = base_slug
    counter = 1

    while True:
        # Buscar si existe este slug
        existing = repo.get_by_slug(slug)
        if existing is None or (exclude_id is not None and existing.id == exclude_id):
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


class CategoriaService:
    """Servicio de categorías."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = CategoriaRepository(session)

    def create(self, data: CategoriaCreate) -> Categoria:
        """
        Crea una nueva categoría.

        Args:
            data: Schema de creación

        Returns:
            Categoría creada

        Raises:
            HTTPException 409: Si el nombre ya existe en el mismo nivel
            HTTPException 404: Si el padre no existe
        """
        # Validar que el padre existe si se proporciona
        padre_id = data.categoria_padre_id
        if padre_id is not None:
            padre = self.repo.get_by_id_active(padre_id)
            if not padre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La categoría padre no existe",
                )

        # Verificar nombre único en el mismo nivel
        if self.repo.exists_by_name_and_parent(data.nombre, padre_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una categoría con este nombre en este nivel",
            )

        # Generar slug único
        base_slug = _generate_slug(data.nombre)
        slug = _ensure_unique_slug(self.repo, base_slug)

        # Crear categoría
        categoria = Categoria(
            nombre=data.nombre,
            slug=slug,
            descripcion=data.descripcion,
            padre_id=padre_id,
            orden=0,  # Por defecto
            activa=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.repo.add(categoria)
        self.session.flush()
        return categoria

    def get_by_id(self, category_id: int) -> Categoria:
        """
        Obtiene una categoría por ID.

        Args:
            category_id: ID de la categoría

        Returns:
            Categoría encontrada

        Raises:
            HTTPException 404: Si no existe o está inactiva
        """
        categoria = self.repo.get_by_id_active(category_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        return categoria

    def list_all(self) -> list[Categoria]:
        """
        Lista todas las categorías activas.

        Returns:
            Lista de categorías ordenadas por orden y nombre
        """
        return self.repo.get_all_active()

    def update(self, category_id: int, data: CategoriaUpdate) -> Categoria:
        """
        Actualiza una categoría.

        Args:
            category_id: ID de la categoría
            data: Schema de actualización

        Returns:
            Categoría actualizada

        Raises:
            HTTPException 404: Si no existe
            HTTPException 409: Si el nombre ya existe en el mismo nivel
            HTTPException 400: Si se crearía un ciclo
        """
        categoria = self.repo.get_by_id_with_trash(category_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        # Verificar si es activa (no se puede editar una eliminada)
        if not categoria.activa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede editar una categoría eliminada",
            )

        # Nuevo padre (0 = sin padre)
        nuevo_padre_id = data.categoria_padre_id
        if nuevo_padre_id == 0:
            nuevo_padre_id = None

        # Validar ciclo si se cambia el padre
        if nuevo_padre_id is not None and nuevo_padre_id != categoria.padre_id:
            # Verificar que el nuevo padre existe y está activo
            nuevo_padre = self.repo.get_by_id_active(nuevo_padre_id)
            if not nuevo_padre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La categoría padre no existe",
                )

            # Verificar ciclo
            if self.repo.check_cycle(category_id, nuevo_padre_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede mover la categoría bajo una de sus descendientes",
                )

        # Verificar nombre único en el mismo nivel
        # Usamos el nuevo padre_id o el actual
        target_parent_id = nuevo_padre_id if nuevo_padre_id is not None else categoria.padre_id

        if data.nombre is not None and data.nombre != categoria.nombre:
            if self.repo.exists_by_name_and_parent(data.nombre, target_parent_id, exclude_id=category_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe una categoría con este nombre en este nivel",
                )

        # Aplicar cambios
        if data.nombre is not None:
            categoria.nombre = data.nombre
            # Regenerar slug
            base_slug = _generate_slug(data.nombre)
            categoria.slug = _ensure_unique_slug(self.repo, base_slug, exclude_id=category_id)

        if data.descripcion is not None:
            categoria.descripcion = data.descripcion

        if nuevo_padre_id is not None:
            categoria.padre_id = nuevo_padre_id

        if data.activa is not None:
            categoria.activa = data.activa

        categoria.updated_at = datetime.utcnow()
        self.session.add(categoria)
        self.session.flush()
        return categoria

    def soft_delete(self, category_id: int) -> None:
        """
        Realiza soft-delete en cascada.

        Args:
            category_id: ID de la categoría

        Raises:
            HTTPException 404: Si no existe
        """
        categoria = self.repo.get_by_id_with_trash(category_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        # No hacer nada si ya está inactiva
        if not categoria.activa:
            return

        self.repo.soft_delete_with_descendants(category_id)

    def get_tree(self) -> list[CategoriaTreeResponse]:
        """
        Construye el árbol completo de categorías.

        Returns:
            Lista de nodos raíz con sus hijos anidados
        """
        # Obtener todas las activas
        all_categorias = self.repo.get_all_active()

        # Crear mapa de hijos por padre
        children_map: dict[Optional[int], list[Categoria]] = {}
        for cat in all_categorias:
            parent = cat.padre_id
            if parent not in children_map:
                children_map[parent] = []
            children_map[parent].append(cat)

        # Ordenar hijos por orden, nombre
        for parent_id in children_map:
            children_map[parent_id].sort(key=lambda c: (c.orden, c.nombre))

        def build_node(categoria: Categoria) -> CategoriaTreeResponse:
            children = children_map.get(categoria.id, [])
            return CategoriaTreeResponse(
                id=categoria.id,
                nombre=categoria.nombre,
                descripcion=categoria.descripcion,
                activa=categoria.activa,
                hijos=[build_node(child) for child in children],
            )

        # Construir nodos raíz
        root_categories = children_map.get(None, [])
        return [build_node(cat) for cat in root_categories]

    def get_subcategorias(self, category_id: int, profundidad: Optional[int] = None) -> list[Categoria]:
        """
        Obtiene los descendientes de una categoría.

        Args:
            category_id: ID de la categoría raíz
            profundidad: Profundidad máxima (None = todos)

        Returns:
            Lista de categorías descendientes

        Raises:
            HTTPException 404: Si la categoría no existe
        """
        categoria = self.repo.get_by_id_active(category_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        return self.repo.get_descendants_cte(category_id, profundidad)