"""
app.modules.usuarios.repository

Repository para gestión de usuarios (admin).
"""
from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.auth.model import Usuario


class UsuariosRepository(BaseRepository[Usuario]):
    """
    Repository para operaciones de administración de usuarios.
    
    Métodos:
    - get_all: listar usuarios con paginación
    - update: actualizar usuario (nombre, rol, telefono, activo)
    - delete: soft delete (marcar como no activo)
    """
    
    def __init__(self, session: Session):
        super().__init__(session, Usuario)
    
    def get_all(
        self,
        offset: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> list[Usuario]:
        """Lista todos los usuarios con paginación."""
        if include_inactive:
            stmt = select(Usuario).offset(offset).limit(limit)
        else:
            stmt = (
                select(Usuario)
                .where(Usuario.activo == True)
                .offset(offset)
                .limit(limit)
            )
        return list(self.session.exec(stmt).all())
    
    def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario (nombre, rol, telefono, activo)."""
        self.session.add(usuario)
        self.session.flush()
        return usuario
    
    def soft_delete(self, usuario: Usuario) -> Usuario:
        """Soft delete — marca al usuario como no activo."""
        usuario.activo = False
        self.session.add(usuario)
        self.session.flush()
        return usuario
    
    def search(self, query: str, offset: int = 0, limit: int = 100) -> list[Usuario]:
        """Busca usuarios por nombre o email."""
        stmt = (
            select(Usuario)
            .where(
                (Usuario.nombre.ilike(f"%{query}%"))
                | (Usuario.email.ilike(f"%{query}%"))
            )
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.exec(stmt).all())
