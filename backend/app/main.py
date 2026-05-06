"""
FastAPI application entry point.
Configuración: CORS, rate limiting, exception handlers, routers.
"""
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings

settings = get_settings()


# Rate limiter - 5 intentos cada 15 minutos por IP
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle de la app: startup y shutdown."""
    # Startup
    yield
    # Shutdown


# FastAPI app
app = FastAPI(
    title="Food Store API",
    description="API REST para sistema de gestión de pedidos de comida",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers RFC 7807
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Maneja HTTPException con formato RFC 7807."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "https://httpstatuses.com/" + str(exc.status_code),
            "title": exc.detail,
            "status": exc.status_code,
            "detail": exc.detail,
        }
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Maneja rate limit exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "type": "https://httpstatuses.com/429",
            "title": "Too Many Requests",
            "status": 429,
            "detail": "Has superado el límite de intentos. Intenta más tarde.",
            "retry_after": exc.detail,
        },
        headers={"Retry-After": str(exc.detail)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales con formato RFC 7807."""
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://httpstatuses.com/500",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "Error interno del servidor",
        }
    )


# Health check
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Endpoint de salud de la aplicación."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Routers de módulos (se importan cuando estén implementados)
# Descomenta según se implementen los módulos:
# from app.modules.auth.router import router as auth_router
# from app.modules.usuarios.router import router as usuarios_router
# from app.modules.categorias.router import router as categorias_router
# from app.modules.productos.router import router as productos_router
# from app.modules.ingredientes.router import router as ingredientes_router
# from app.modules.direcciones.router import router as direcciones_router
# from app.modules.pedidos.router import router as pedidos_router
# from app.modules.pagos.router import router as pagos_router
# from app.modules.admin.router import router as admin_router

# Registro de routers con prefijo /api/v1
# app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
# app.include_router(usuarios_router, prefix="/api/v1", tags=["usuarios"])
# app.include_router(categorias_router, prefix="/api/v1", tags=["categorias"])
# app.include_router(productos_router, prefix="/api/v1", tags=["productos"])
# app.include_router(ingredientes_router, prefix="/api/v1", tags=["ingredientes"])
# app.include_router(direcciones_router, prefix="/api/v1", tags=["direcciones"])
# app.include_router(pedidos_router, prefix="/api/v1", tags=["pedidos"])
# app.include_router(pagos_router, prefix="/api/v1", tags=["pagos"])
# app.include_router(admin_router, prefix="/api/v1", tags=["admin"])


# Exportar limiter para usar en routers
__all__ = ["app", "limiter"]