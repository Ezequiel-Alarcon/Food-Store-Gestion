"""
app.modules.perfil.router

Router para gestión del perfil propio del usuario autenticado.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_user
from app.modules.auth.model import Usuario
from app.modules.auth.schemas import ChangePasswordRequest, UpdateProfileRequest
from app.modules.perfil.service import PerfilService

router = APIRouter()


@router.get(
    "/perfil",
    summary="Ver perfil propio",
    description="Devuelve los datos del perfil del usuario autenticado.",
)
async def get_perfil(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
) -> dict:
    """Ver perfil del usuario autenticado."""
    service = PerfilService(session)
    return service.get_perfil(current_user)


@router.put(
    "/perfil",
    summary="Actualizar perfil propio",
    description="Actualiza nombre y/o teléfono del usuario autenticado.",
)
async def update_perfil(
    body: UpdateProfileRequest,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
) -> dict:
    """
    Actualiza perfil propio.
    
    - **nombre**: Nuevo nombre (opcional)
    - **telefono**: Nuevo teléfono (opcional)
    """
    service = PerfilService(session)
    return service.update_perfil(current_user, body)


@router.put(
    "/perfil/password",
    summary="Cambiar contraseña",
    description="Cambia la contraseña del usuario autenticado.",
)
async def change_password(
    body: ChangePasswordRequest,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
) -> dict:
    """
    Cambia la contraseña del usuario autenticado.
    
    - **current_password**: Contraseña actual
    - **new_password**: Nueva contraseña (mínimo 8 caracteres)
    """
    service = PerfilService(session)
    return service.change_password(current_user, body)
