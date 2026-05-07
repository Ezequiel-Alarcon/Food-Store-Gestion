"""app.core.database

Configuración de base de datos con SQLModel.

Expone:
- `engine`
- `SessionLocal`: factory de sesiones (por request / por UnitOfWork)
- `get_session`: dependencia FastAPI para obtener una Session por request
"""

from typing import Generator

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

# Engine con pool de conexiones
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory para UoW pattern
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def get_session() -> Generator[Session, None, None]:
    """
    Generador de sesión para inyección de dependencias.
    Uso: Depends(get_session)
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Inicializa la base de datos creando todas las tablas."""
    SQLModel.metadata.create_all(engine)
