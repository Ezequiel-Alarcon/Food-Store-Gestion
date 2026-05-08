"""
app.modules.usuarios.router

Router para gestión administrativa de usuarios.
Solo accesible por ADMIN y GESTOR.
"""

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_user, require_role
from app.modules.auth.model import Usuario
from app.modules.usuarios.service import UsuariosService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get(
    "/",
    summary="Listar usuarios",
    description="Lista todos los usuarios. Acceso: ADMIN, GESTOR.",
)
async def list_users(
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    include_inactive: bool = Query(False, description="Incluir usuarios inactivos"),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(
        require_role("ADMIN", "GESTOR")
    ),
) -> list[dict]:
    """Lista todos los usuarios (ADMIN/GESTOR)."""
    service = UsuariosService(session)
    usuarios = service.list_users(
        offset=offset,
        limit=limit,
        include_inactive=include_inactive,
    )
    return [
        {
            "id": u.id,
            "email": u.email,
            "nombre": u.nombre,
            "rol": u.rol,
            "telefono": u.telefono,
            "activo": u.activo,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in usuarios
    ]


@router.get(
    "/{user_id}",
    summary="Ver usuario",
    description="Obtiene un usuario por ID. Acceso: ADMIN, GESTOR.",
)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(
        require_role("ADMIN", "GESTOR")
    ),
) -> dict:
    """Obtiene un usuario por ID (ADMIN/GESTOR)."""
    service = UsuariosService(session)
    usuario = service.get_user(user_id)
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "telefono": usuario.telefono,
        "activo": usuario.activo,
        "created_at": usuario.created_at.isoformat() if usuario.created_at else None,
    }


@router.put(
    "/{user_id}",
    summary="Actualizar usuario",
    description="Actualiza datos de un usuario. Acceso: ADMIN.",
)
async def update_user(
    user_id: int,
    nombre: str | None = Query(None, description="Nuevo nombre"),
    rol: str | None = Query(None, description="Nuevo rol"),
    telefono: str | None = Query(None, description="Nuevo teléfono"),
    activo: bool | None = Query(None, description="Estado activo"),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_role("ADMIN")),
) -> dict:
    """Actualiza un usuario (solo ADMIN)."""
    service = UsuariosService(session)
    usuario = service.update_user(
        user_id=user_id,
        nombre=nombre,
        rol=rol,
        telefono=telefono,
        activo=activo,
    )
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "telefono": usuario.telefono,
        "activo": usuario.activo,
    }


@router.delete(
    "/{user_id}",
    summary="Desactivar usuario",
    description="Desactiva un usuario (soft delete). Acceso: ADMIN.",
)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_role("ADMIN")),
) -> dict:
    """Desactiva un usuario (soft delete, solo ADMIN)."""
    service = UsuariosService(session)
    service.deactivate_user(user_id)
    return {"message": "Usuario desactivado correctamente"}
