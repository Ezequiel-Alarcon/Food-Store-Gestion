"""
app.modules.usuarios.service

Servicio para gestión administrativa de usuarios.
"""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.auth.model import Usuario
from app.modules.usuarios.repository import UsuariosRepository


class UsuariosService:
    """
    Servicio de administración de usuarios.
    Permite CRUD de usuarios por ADMIN/GESTOR.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuariosRepository(session)
    
    def list_users(
        self,
        offset: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> list[Usuario]:
        """Lista todos los usuarios."""
        return self.repo.get_all(
            offset=offset,
            limit=limit,
            include_inactive=include_inactive,
        )
    
    def get_user(self, user_id: int) -> Usuario:
        """Obtiene un usuario por ID."""
        usuario = self.repo.get_by_id(user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return usuario
    
    def update_user(
        self,
        user_id: int,
        nombre: str | None = None,
        rol: str | None = None,
        telefono: str | None = None,
        activo: bool | None = None,
    ) -> Usuario:
        """Actualiza campos del usuario."""
        usuario = self.get_user(user_id)
        
        if nombre is not None:
            usuario.nombre = nombre
        if rol is not None:
            usuario.rol = rol
        if telefono is not None:
            usuario.telefono = telefono
        if activo is not None:
            usuario.activo = activo
        
        return self.repo.update(usuario)
    
    def deactivate_user(self, user_id: int) -> Usuario:
        """Desactiva un usuario (soft delete)."""
        usuario = self.get_user(user_id)
        return self.repo.soft_delete(usuario)
    
    def search_users(self, query: str, offset: int = 0, limit: int = 100) -> list[Usuario]:
        """Busca usuarios por nombre o email."""
        return self.repo.search(query, offset=offset, limit=limit)
