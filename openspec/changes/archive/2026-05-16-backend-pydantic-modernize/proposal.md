## Why

Pydantic v2 (desde 2023) deprecó la clase interna `Config` en favor de `model_config = ConfigDict(...)`. Esto no es solo stylístico — `ConfigDict` es más performante, permite configuración por defecto a nivel módulo, y es el path oficial de migración hacia Pydantic v3.

**Problema:** El codebase actual usa `class Config: from_attributes = True` en 13 lugares. Esto genera warnings de deprecación en Pydantic 2.x y bloquea la migración a Pydantic 3.

## What Changes

- Reemplazar `class Config: ...` → `model_config = ConfigDict(...)` en todos los schemas del backend
- 13 usages distribuidos en 6 archivos:
  - `productos/schemas.py` (5 usages)
  - `sucursales/schemas.py` (1)
  - `ingredientes/schemas.py` (2)
  - `direcciones/schemas.py` (2)
  - `categorias/schemas.py` (2)
  - `core/schemas.py` (1)
- **No hay cambios de comportamiento** — solo refactor de configuración de schemas

## Capabilities

### Modified Capabilities

- `backend-pydantic-modernize`: Migración interna — no modifica specs existentes (es deuda técnica de implementación, no cambio de requisitos)

## Impact

**Archivos afectados (6 archivos, 13 usages):**

| Módulo | Archivo | Usages |
|--------|---------|--------|
| `productos` | `schemas.py` | 5 |
| `sucursales` | `schemas.py` | 1 |
| `ingredientes` | `schemas.py` | 2 |
| `direcciones` | `schemas.py` | 2 |
| `categorias` | `schemas.py` | 2 |
| `core` | `schemas.py` | 1 |

**Dependencias:** Ninguna — no requiere cambios en models, services, routers ni API.