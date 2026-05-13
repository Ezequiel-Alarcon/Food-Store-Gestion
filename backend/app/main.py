"""
FastAPI application entry point.
Configuración: CORS, rate limiting, exception handlers, routers.
"""
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import get_settings
from app.core.exceptions import (
    AppError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
    ValidationError,
)
from app.core.middleware import ErrorHandlerMiddleware
from app.core.limiter import limiter

settings = get_settings()


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

# Rate limiting state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Rate limiting middleware (must be added for @limiter.limit() to work)
app.add_middleware(SlowAPIMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling middleware (must be last to catch all exceptions)
app.add_middleware(ErrorHandlerMiddleware)


# Exception handlers RFC 7807
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Maneja excepciones custom de la app con formato RFC 7807."""
    instance = request.url.path
    problem = exc.to_problem_detail(debug=settings.DEBUG)
    problem["instance"] = instance
    return JSONResponse(status_code=exc.status_code, content=problem)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Maneja HTTPException con formato RFC 7807."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "https://httpstatuses.com/" + str(exc.status_code),
            "title": exc.detail,
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": request.url.path,
        }
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Maneja rate limit exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "type": "https://httpstatuses.com/429",
            "title": "Too Many Requests",
            "status": 429,
            "detail": "Has superado el límite de solicitudes. Intenta más tarde.",
            "instance": request.url.path,
        },
        headers={"Retry-After": str(exc.detail)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Maneja excepciones generales con formato RFC 7807."""
    import sys
    import traceback

    exc_info = "".join(traceback.format_exception(*sys.exc_info()))
    print(f"[ERROR] Unhandled exception: {exc}", file=sys.stderr)
    print(exc_info, file=sys.stderr)

    if settings.DEBUG:
        detail = exc_info
    else:
        detail = "Error interno del servidor"

    return JSONResponse(
        status_code=500,
        content={
            "type": "https://httpstatuses.com/500",
            "title": "Internal Server Error",
            "status": 500,
            "detail": detail,
            "instance": request.url.path,
        }
    )


# Health check (excluido de rate limiting)
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Endpoint de salud de la aplicación."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Routers de módulos (se importan cuando estén implementados)
from app.modules.auth.router import router as auth_router
from app.modules.usuarios.router import router as usuarios_router
from app.modules.perfil.router import router as perfil_router
from app.modules.categorias.router import router as categorias_router
from app.modules.direcciones.router import router as direcciones_router
from app.modules.sucursales.router import router as sucursales_router
from app.modules.productos.router import router as productos_router
from app.modules.ingredientes.router import router as ingredientes_router
from app.modules.pedidos.router import router as pedidos_router
from app.modules.pagos.router import router as pagos_router
from app.modules.admin.router import router as admin_router

# Registro de routers con prefijo /api/v1
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(usuarios_router, prefix="/api/v1", tags=["usuarios"])
app.include_router(perfil_router, prefix="/api/v1", tags=["perfil"])
app.include_router(categorias_router, prefix="/api/v1", tags=["categorias"])

app.include_router(direcciones_router, prefix="/api/v1", tags=["direcciones"])
app.include_router(sucursales_router, prefix="/api/v1", tags=["branches"])

app.include_router(ingredientes_router, prefix="/api/v1", tags=["ingredientes"])

app.include_router(productos_router, prefix="/api/v1/productos", tags=["productos"])
app.include_router(pedidos_router, prefix="/api/v1/pedidos", tags=["pedidos"])
app.include_router(pagos_router, prefix="/api/v1/pagos", tags=["pagos"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])


# Exportar limiter para usar en routers
__all__ = ["app", "limiter"]
