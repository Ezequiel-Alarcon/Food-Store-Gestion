"""
app.modules.categorias.router

Router para endpoints de categorías.
"""

from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_user, require_role
from app.modules.categorias.schemas import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaTreeResponse,
    CategoriaUpdate,
)
from app.modules.categorias.service import CategoriaService

router = APIRouter()


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría",
    description="Crea una nueva categoría. Requiere rol ADMIN.",
)
def create_categoria(
    data: CategoriaCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> CategoriaResponse:
    """Crea una nueva categoría."""
    service = CategoriaService(session)
    categoria = service.create(data)
    return CategoriaResponse(
        id=categoria.id,
        nombre=categoria.nombre,
        descripcion=categoria.descripcion,
        categoria_padre_id=categoria.padre_id,
        activa=categoria.activa,
    )


@router.get(
    "/",
    response_model=list[CategoriaResponse],
    summary="Listar categorías",
    description="Lista todas las categorías activas. Requiere autenticación.",
)
def list_categorias(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[CategoriaResponse]:
    """Lista todas las categorías activas."""
    service = CategoriaService(session)
    categorias = service.list_all()
    return [
        CategoriaResponse(
            id=cat.id,
            nombre=cat.nombre,
            descripcion=cat.descripcion,
            categoria_padre_id=cat.padre_id,
            activa=cat.activa,
        )
        for cat in categorias
    ]


@router.get(
    "/arbol",
    response_model=list[CategoriaTreeResponse],
    summary="Obtener árbol de categorías",
    description="Obtiene el árbol completo de categorías. Requiere autenticación.",
)
def get_arbol(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[CategoriaTreeResponse]:
    """Obtiene el árbol completo de categorías."""
    service = CategoriaService(session)
    return service.get_tree()


@router.get(
    "/publico/arbol",
    response_model=list[CategoriaTreeResponse],
    summary="Obtener árbol público de categorías",
    description="Obtiene el árbol completo de categorías sin autenticación.",
)
def get_arbol_publico(
    session: Session = Depends(get_session),
) -> list[CategoriaTreeResponse]:
    """Obtiene el árbol público de categorías (sin auth)."""
    service = CategoriaService(session)
    return service.get_tree()


@router.get(
    "/{category_id}",
    response_model=CategoriaResponse,
    summary="Obtener categoría",
    description="Obtiene una categoría por ID. Requiere autenticación.",
)
def get_categoria(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> CategoriaResponse:
    """Obtiene una categoría por ID."""
    service = CategoriaService(session)
    categoria = service.get_by_id(category_id)
    return CategoriaResponse(
        id=categoria.id,
        nombre=categoria.nombre,
        descripcion=categoria.descripcion,
        categoria_padre_id=categoria.padre_id,
        activa=categoria.activa,
    )


@router.get(
    "/{category_id}/subcategorias",
    response_model=list[CategoriaResponse],
    summary="Obtener subcategorías",
    description="Obtiene los descendientes de una categoría. Requiere autenticación.",
)
def get_subcategorias(
    category_id: int,
    profundidad: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[CategoriaResponse]:
    """Obtiene las subcategorías de una categoría."""
    service = CategoriaService(session)
    subcategorias = service.get_subcategorias(category_id, profundidad)
    return [
        CategoriaResponse(
            id=cat.id,
            nombre=cat.nombre,
            descripcion=cat.descripcion,
            categoria_padre_id=cat.padre_id,
            activa=cat.activa,
        )
        for cat in subcategorias
    ]


@router.put(
    "/{category_id}",
    response_model=CategoriaResponse,
    summary="Actualizar categoría",
    description="Actualiza una categoría existente. Requiere rol ADMIN.",
)
def update_categoria(
    category_id: int,
    data: CategoriaUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> CategoriaResponse:
    """Actualiza una categoría."""
    service = CategoriaService(session)
    categoria = service.update(category_id, data)
    return CategoriaResponse(
        id=categoria.id,
        nombre=categoria.nombre,
        descripcion=categoria.descripcion,
        categoria_padre_id=categoria.padre_id,
        activa=categoria.activa,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar categoría",
    description="Elimina (soft-delete) una categoría y sus descendientes. Requiere rol ADMIN.",
)
def delete_categoria(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> None:
    """Elimina (soft-delete) una categoría en cascada."""
    service = CategoriaService(session)
    service.soft_delete(category_id)
    return None