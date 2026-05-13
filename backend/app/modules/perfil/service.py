"""
app.modules.perfil.service

Servicio para gestión del perfil propio del usuario autenticado.
"""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import hash_password, verify_password
from app.modules.auth.model import Usuario
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import ChangePasswordRequest, UpdateProfileRequest
from app.modules.refreshtokens.repository import RefreshTokenRepository


class PerfilService:
    """
    Servicio de perfil propio.
    Permite ver, editar y cambiar contraseña del usuario autenticado.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.auth_repo = AuthRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)
    
    def get_perfil(self, usuario: Usuario) -> dict:
        """Devuelve los datos del perfil del usuario."""
        return {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "rol": usuario.rol.value if hasattr(usuario.rol, "value") else usuario.rol,
            "telefono": usuario.telefono,
            "activo": usuario.activo,
            "created_at": usuario.created_at.isoformat() if usuario.created_at else None,
        }

    def update_perfil(self, usuario: Usuario, request: UpdateProfileRequest) -> dict:
        """Actualiza nombre, apellido y/o teléfono del usuario."""
        if request.nombre is not None:
            usuario.nombre = request.nombre
        if request.apellido is not None:
            usuario.apellido = request.apellido
        if request.telefono is not None:
            usuario.telefono = request.telefono

        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)

        return self.get_perfil(usuario)

    def change_password(self, usuario: Usuario, request: ChangePasswordRequest) -> dict:
        """Cambia la contraseña del usuario e invalida todos los refresh tokens."""

        # Verificar contraseña actual
        if not verify_password(request.current_password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta",
            )

        # Verificar que la nueva no sea igual a la actual (defense in depth)
        if request.new_password == request.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña no puede ser igual a la actual",
            )

        # Hashear nueva contraseña
        usuario.password_hash = hash_password(request.new_password)
        self.session.add(usuario)
        self.session.flush()

        # Invalidar TODOS los refresh tokens del usuario (RN-AU05, US-063)
        self.refresh_repo.revoke_all_by_user(usuario.id)

        return {"message": "Contraseña actualizada correctamente"}
