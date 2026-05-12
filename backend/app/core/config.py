"""
Configuración de la aplicación usando pydantic-settings.
Carga variables de entorno desde .env file.
"""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/foodstore_db",
        description="URL de conexión a PostgreSQL"
    )

    # Security
    SECRET_KEY: str = Field(
        default="your-super-secret-key-min-32-chars-here",
        description="Clave secreta para firmar JWT"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Algoritmo JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Expiración del access token en minutos"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Expiración del refresh token en días"
    )

    # CORS
    CORS_ORIGINS: str = Field(
        default='["http://localhost:5173"]',
        description="Orígenes permitidos para CORS (JSON array)"
    )

    # MercadoPago
    MP_ACCESS_TOKEN: str = Field(
        default="",
        description="Access Token de MercadoPago"
    )
    MP_PUBLIC_KEY: str = Field(
        default="",
        description="Public Key de MercadoPago para el frontend"
    )
    MP_NOTIFICATION_URL: str = Field(
        default="",
        description="URL del webhook IPN de MercadoPago"
    )
    MP_WEBHOOK_SECRET: str = Field(
        default="",
        description="Webhook secret para validar firmas de MercadoPago (opcional)"
    )

    # Environment
    ENVIRONMENT: str = Field(
        default="development",
        description="Entorno de ejecución"
    )
    DEBUG: bool = Field(
        default=True,
        description="Modo debug"
    )

    # Rate limiting
    RATE_LIMIT_PUBLIC: int = Field(
        default=60,
        description="Requests por minuto para endpoints públicos"
    )
    RATE_LIMIT_AUTHENTICATED: int = Field(
        default=100,
        description="Requests por minuto para endpoints autenticados"
    )
    RATE_LIMIT_AUTH: int = Field(
        default=5,
        description="Requests por minuto para endpoints de auth por IP"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parsea CORS_ORIGINS de string JSON a lista."""
        import json
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    """Retorna settings cacheado (singleton)."""
    return Settings()