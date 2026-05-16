## Why

`datetime.utcnow()` está deprecated desde Python 3.12 y genera warnings en Python 3.11+. El reemplazo correcto es `datetime.now(timezone.utc)` que retorna un timezone-aware datetime evitando ambiguedades en comparaciones y serialización.

**Problema técnico:** `utcnow()` retorna un naive datetime (sin timezone) que se interpreta como UTC por convención, pero Python no lo sabe — esto causa bugs sutiles en comparaciones con timezone-aware datetimes y posibles issues en serialización JSON.

**Estado actual del codebase:** 21 usages de `datetime.utcnow()` en módulos activos (`productos`, `sucursales`, `direcciones`) que deben migrarse.

## What Changes

- Reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en todos los archivos del backend
- Imports: agregar `timezone` de `datetime` donde sea necesario
- **No hay cambios de comportamiento** — solo refactor de dependencias de tiempo

## Capabilities

### Modified Capabilities

- `backend-datetime-fix`: Migración interna — no modifica specs existentes (es deuda técnica de implementación, no cambio de requisitos)

## Impact

**Archivos afectados (21 usages en código de producción):**

| Módulo | Archivo | Usages |
|--------|---------|--------|
| `productos` | `service.py` | 2 |
| `productos` | `repository.py` | 6 |
| `sucursales` | `service.py` | 3 |
| `direcciones` | `service.py` | 10 |

**Nota:** Los archivos en `.agents/skills/` son templates de referencia y no se incluyen en esta migración.

**Dependencias:** Ninguna — no requiere cambios en schemas, tests ni API.