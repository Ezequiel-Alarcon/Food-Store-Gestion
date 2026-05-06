## Why

El proyecto Food Store necesita una base de infraestructura backend funcional antes de implementar cualquier módulo de negocio. Sin FastAPI configurado, conexión a PostgreSQL, migraciones Alembic y seed data, los cambios posteriores no podrán probarse ni ejecutarse. Este change establece la fundación técnica.

## What Changes

- **backend/app/main.py**: FastAPI app con CORS, rate limiting (slowapi), errores RFC 7807
- **backend/app/core/config.py**: Carga de variables de entorno con Pydantic Settings
- **backend/app/core/database.py**: SQLModel Engine + SessionLocal para PostgreSQL
- **backend/app/core/security.py**: Password hashing con bcrypt (cost 12), JWT utils
- **backend/app/db/**: Estructura Alembic con alembic.ini y migrations/
- **backend/app/db/seed.py**: Script de seed con Roles, EstadosPedido, FormaPago, usuario admin
- **backend/app/models/**: Modelos SQLModel existentes en módulos + setup de inicialización

## Capabilities

### New Capabilities
- **fastapi-app**: FastAPI configurado con CORS, rate limiting, exception handlers
- **database-connection**: SQLModel + PostgreSQL con engine y session factory
- **alembic-migrations**: Migraciones versionadas con Alembic
- **seed-data**: Datos iniciales obligatorios (Roles, Estados, FormasPago, admin)

### Modified Capabilities
- Ninguna (es la base inicial)

## Impact

- Backend: nuevo archivo main.py, core/, db/
- Dependencias: fastapi, uvicorn, sqlmodel, alembic, passlib, python-jose, slowapi
- Seed: ejecuta después de `alembic upgrade head`