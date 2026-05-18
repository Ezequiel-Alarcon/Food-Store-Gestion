"""
app.modules.auth.router

Router para endpoints de autenticación.
"""

from fastapi import APIRouter, Depends, Request, Response, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.config import get_settings
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.modules.auth.schemas import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService

router = APIRouter()
settings = get_settings()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario con rol CLIENT y devuelve tokens JWT. Rate limited: 5 intentos/15 minutos.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH}/15minutes")
async def register(
    request: Request,
    body: RegisterRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Registra un nuevo usuario.
    
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    - **nombre**: Nombre
    - **apellido**: Apellido
    - **telefono**: Teléfono opcional en formato E.164
    """
    service = AuthService(session)
    return service.register(body)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve tokens JWT. Rate limited: 5 intentos/15 minutos.",
)
@limiter.limit(f"{settings.RATE_LIMIT_AUTH}/15minutes")
async def login(
    request: Request,
    body: LoginRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Inicia sesión con email y password.
    
    - **email**: Email registrado
    - **password**: Contraseña
    """
    service = AuthService(session)
    return service.login(body)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Renovar access token",
    description="Renueva el access token usando un refresh token válido.",
)
async def refresh(
    body: RefreshRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Renueva access token.
    
    - **refresh_token**: Token de renovación válido
    """
    service = AuthService(session)
    return service.refresh_token(body)


@router.post(
    "/logout",
    status_code=204,
    summary="Cerrar sesión",
    description="Invalida el refresh token proporcionado.",
)
async def logout(
    body: RefreshRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Cierra sesión revocando el refresh token.
    
    - **refresh_token**: Token a revocar
    """
    service = AuthService(session)
    service.logout(body.refresh_token)
    return Response(status_code=204)
