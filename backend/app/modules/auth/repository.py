"""
app.modules.auth.repository

Repository para operaciones de autenticación y usuarios.
"""
from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.modules.auth.model import Usuario


class AuthRepository(BaseRepository[Usuario]):
    """
    Repository para operaciones de usuario y autenticación.
    
    Hereda de BaseRepository[Usuario] y agrega métodos específicos:
    - get_user_by_email
    - create_user
    """
    
    def __init__(self, session: Session):
        super().__init__(session, Usuario)
    
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email (case-insensitive)."""
        stmt = select(Usuario).where(Usuario.email == email.lower())
        return self.session.exec(stmt).first()
    
    def get_user_by_email_optional(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email (case-insensitive)."""
        stmt = select(Usuario).where(Usuario.email == email.lower())
        return self.session.exec(stmt).first()
    
    def create_user(
        self,
        email: str,
        nombre: str,
        password_hash: str,
        apellido: str = "",
        rol: str = "CLIENT",
        telefono: Optional[str] = None,
    ) -> Usuario:
        """Crea un nuevo usuario."""
        usuario = Usuario(
            email=email.lower(),
            nombre=nombre,
            apellido=apellido,
            password_hash=password_hash,
            rol=rol,
            telefono=telefono,
            activo=True,
        )
        self.session.add(usuario)
        self.session.flush()
        return usuario
    
    def get_active_users(self, offset: int = 0, limit: int = 100) -> list[Usuario]:
        """Lista usuarios activos."""
        stmt = select(Usuario).where(Usuario.activo == True).offset(offset).limit(limit)
        return list(self.session.exec(stmt).all())
    
    def count_active(self) -> int:
        """Cuenta usuarios activos."""
        stmt = select(Usuario).where(Usuario.activo == True)
        return len(list(self.session.exec(stmt).all()))