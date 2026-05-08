"""
app.modules.ingredientes.router

Router para endpoints de ingredientes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_user, require_role
from app.modules.ingredientes.schemas import (
    IngredienteCreate,
    IngredienteResponse,
    IngredienteUpdate,
)
from app.modules.ingredientes.service import IngredienteService

router = APIRouter()


@router.post(
    "/",
    response_model=IngredienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ingrediente",
    description="Crea un nuevo ingrediente. Requiere rol ADMIN o STOCK.",
)
def create_ingrediente(
    data: IngredienteCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> IngredienteResponse:
    """Crea un nuevo ingrediente."""
    service = IngredienteService(session)
    ingrediente = service.create(data)
    return IngredienteResponse(
        id=ingrediente.id,
        nombre=ingrediente.nombre,
        descripcion=ingrediente.descripcion,
        es_alergeno=ingrediente.es_alergeno,
        creado_en=ingrediente.creado_en.isoformat() if ingrediente.creado_en else "",
        actualizado_en=ingrediente.actualizado_en.isoformat() if ingrediente.actualizado_en else None,
    )


@router.get(
    "/",
    response_model=list[IngredienteResponse],
    summary="Listar ingredientes",
    description="Lista todos los ingredientes activos con paginación. Todos los roles autenticados.",
)
def list_ingredientes(
    skip: int = Query(default=0, ge=0, description="Offset para paginación"),
    limit: int = Query(default=20, ge=1, le=100, description="Límite de resultados"),
    es_alergeno: Optional[bool] = Query(default=None, description="Filtrar por alérgenos"),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[IngredienteResponse]:
    """Lista todos los ingredientes activos."""
    service = IngredienteService(session)
    ingredientes, _ = service.list(skip=skip, limit=limit, es_alergeno=es_alergeno)
    return [
        IngredienteResponse(
            id=ing.id,
            nombre=ing.nombre,
            descripcion=ing.descripcion,
            es_alergeno=ing.es_alergeno,
            creado_en=ing.creado_en.isoformat() if ing.creado_en else "",
            actualizado_en=ing.actualizado_en.isoformat() if ing.actualizado_en else None,
        )
        for ing in ingredientes
    ]


@router.get(
    "/{ingrediente_id}",
    response_model=IngredienteResponse,
    summary="Obtener ingrediente",
    description="Obtiene un ingrediente por ID. Todos los roles autenticados.",
)
def get_ingrediente(
    ingrediente_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> IngredienteResponse:
    """Obtiene un ingrediente por ID."""
    service = IngredienteService(session)
    ingrediente = service.get_by_id(ingrediente_id)
    return IngredienteResponse(
        id=ingrediente.id,
        nombre=ingrediente.nombre,
        descripcion=ingrediente.descripcion,
        es_alergeno=ingrediente.es_alergeno,
        creado_en=ingrediente.creado_en.isoformat() if ingrediente.creado_en else "",
        actualizado_en=ingrediente.actualizado_en.isoformat() if ingrediente.actualizado_en else None,
    )


@router.patch(
    "/{ingrediente_id}",
    response_model=IngredienteResponse,
    summary="Actualizar ingrediente",
    description="Actualiza un ingrediente existente (actualización parcial). Requiere rol ADMIN o STOCK.",
)
def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> IngredienteResponse:
    """Actualiza un ingrediente (PATCH - campos opcionales)."""
    service = IngredienteService(session)
    ingrediente = service.update(ingrediente_id, data)
    return IngredienteResponse(
        id=ingrediente.id,
        nombre=ingrediente.nombre,
        descripcion=ingrediente.descripcion,
        es_alergeno=ingrediente.es_alergeno,
        creado_en=ingrediente.creado_en.isoformat() if ingrediente.creado_en else "",
        actualizado_en=ingrediente.actualizado_en.isoformat() if ingrediente.actualizado_en else None,
    )


@router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ingrediente",
    description="Elimina (soft-delete) un ingrediente. Requiere rol ADMIN o STOCK.",
)
def delete_ingrediente(
    ingrediente_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> None:
    """Elimina (soft-delete) un ingrediente."""
    service = IngredienteService(session)
    service.soft_delete(ingrediente_id)
    return None