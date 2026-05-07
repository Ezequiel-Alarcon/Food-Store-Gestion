"""app.core.deps

Dependencias FastAPI para auth/RBAC.

Estas dependencias están pensadas para usarse en routers:

- `get_current_user`: resuelve el principal desde JWT
- `require_role(*roles)`: fuerza RBAC a nivel endpoint

Nota: Si los modelos de identidad (Usuario/Rol) aún no existen, el principal
queda representado por el payload del JWT. Cuando exista el modelo, se puede
reemplazar el retorno por la entidad sin cambiar la firma del router.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _extract_roles(payload: dict[str, Any]) -> set[str]:
    roles = payload.get("roles") or payload.get("role") or []
    if isinstance(roles, str):
        return {roles}
    if isinstance(roles, (list, tuple, set)):
        return {str(r) for r in roles}
    return set()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Any:
    """Resuelve el usuario/principal actual desde JWT.

    Reglas:
    - Si falta token o es inválido/expirado -> 401
    - Si el token tiene `type` y no es `access` -> 401
    - Si existe el modelo `Usuario`, intenta resolverlo por `sub`.
      Si no existe, retorna el payload del JWT como principal.
    """

    try:
        payload = decode_token(token)
    except (ValueError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_type = payload.get("type")
    if token_type is not None and token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Mejor esfuerzo: si existe el modelo Usuario, lo resolvemos.
    try:
        from app.modules.auth.model import Usuario  # type: ignore

        user = session.get(Usuario, sub)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except ImportError:
        return payload


def require_role(*roles: str) -> Callable[[Any], Any]:
    """Devuelve una dependencia que exige al menos uno de los roles."""

    required = {r for r in roles if r}

    def _dep(current_user: Any = Depends(get_current_user)) -> Any:
        # Payload dict (modo sin modelo Usuario)
        if isinstance(current_user, dict):
            user_roles = _extract_roles(current_user)
        else:
            # Modelo: intentamos distintas convenciones sin acoplar fuerte.
            user_roles = set()
            role_value: Optional[Any] = getattr(current_user, "role", None)
            roles_value: Optional[Any] = getattr(current_user, "roles", None)
            if role_value is not None:
                user_roles |= _extract_roles({"role": role_value})
            if roles_value is not None:
                user_roles |= _extract_roles({"roles": roles_value})

        if required and user_roles.isdisjoint(required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado",
            )
        return current_user

    return _dep
