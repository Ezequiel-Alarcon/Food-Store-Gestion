## Why

Durante la implementación de `docker-setup` se descubrieron bugs preexistentes que impiden que el backend FastAPI arranque. El más crítico es un error de resolución de forward references en `auth/router.py` que causa que Pydantic v2 falle al importar los routers. Sin este fix, `docker compose up` levanta la DB y el frontend pero el backend crashea en startup.

## What Changes

- **Fix `auth/router.py`**: Eliminar `from __future__ import annotations` que causa que Pydantic v2 no pueda resolver `LoginRequest` y otros tipos al decorar las rutas FastAPI. El mismo fix se aplica a cualquier otro router que tenga el mismo patrón.
- **Fix `db/seed.py`**: Hacer condicionales los imports de modelos que aún no están implementados (`Rol`, `UsuarioRol`, `EstadoPedido`, `FormaPago`). Si el módulo no existe, el seed omite esa parte en vez de crashear.
- **Documentar fixes ya aplicados**: `requirements.txt` (eliminado `python-cors`, actualizado `python-multipart`), migraciones (renumerado `003` duplicado).

## Capabilities

### Modified Capabilities

Ninguna. Este change no modifica requisitos funcionales — solo corrige bugs de implementación que impedían el startup. El comportamiento esperado de los specs existentes no cambia.

## Impact

- **Archivos modificados**:
  - `backend/app/modules/auth/router.py` — eliminar `from __future__ import annotations`
  - `backend/app/db/seed.py` — imports condicionales con try/except
  - `backend/requirements.txt` — ya corregido (documentar)
  - `backend/app/db/migrations/versions/004_create_sucursales_and_addresses.py` — ya renumerado (documentar)
- **Dependencias**: Ninguna nueva
- **Sin breaking changes**: El comportamiento de la API no cambia
