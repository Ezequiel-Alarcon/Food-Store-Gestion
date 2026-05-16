## Context

Pydantic v2 introduce `ConfigDict` como remplazo de la clase interna `Config`. El codebase actual tiene 13 usages de `class Config: from_attributes = True` que generan warnings de deprecación.

El cambio es mecánico: `class Config: from_attributes = True` → `model_config = ConfigDict(from_attributes=True)`

## Goals / Non-Goals

**Goals:**
- Eliminar todos los `class Config` en schemas del backend
- Usar `ConfigDict` que es el path oficial hacia Pydantic v3
- No alterar comportamiento de serialización/deserialización

**Non-Goals:**
- No modificar schemas de auth (ya usan Pydantic v2 moderno con `model_validator`)
- No modificar lógica de negocio — solo configuración de schemas
- No crear migraciones de API

## Decisions

### Decision 1: Reemplazo uno a uno

**Elección:** Reemplazar cada `class Config: from_attributes = True` por `model_config = ConfigDict(from_attributes=True)` archivo por archivo.

**Alternativas:**
- Migrar automáticamente con script: posible pero overkill para 13 usages
- Definir un `BaseSchema` con `model_config = ConfigDict(from_attributes=True)` y heredar: introduce indirección innecesaria y rompe la convención actual

**Rationale:** Cambio simple y trazable — cada occurrence es visible y auditable.

### Decision 2: Solo `from_attributes = True`

**Elección:** Solo convertir el único flag usado actualmente. No agregar `populate_by_name` u otros flags.

**Rationale:** El scope es limitado — solo `from_attributes` está en uso. Otros flags pueden evaluarse en futuros cambios.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Olvidar algún usage | Verificar con grep post-reemplazo que no quedan `class Config:` en `app/modules/**/schemas.py` y `app/core/schemas.py` |
| Romper serialización | Solo cambia la configuración, no la estructura de datos |

## Migration Plan

1. Reemplazar en `backend/app/core/schemas.py` (1 usage)
2. Reemplazar en `backend/app/modules/productos/schemas.py` (5 usages)
3. Reemplazar en `backend/app/modules/sucursales/schemas.py` (1 usage)
4. Reemplazar en `backend/app/modules/ingredientes/schemas.py` (2 usages)
5. Reemplazar en `backend/app/modules/direcciones/schemas.py` (2 usages)
6. Reemplazar en `backend/app/modules/categorias/schemas.py` (2 usages)
7. Verificar: `grep -r "class Config:" backend/app/modules/**/schemas.py backend/app/core/schemas.py` debe retornar 0 resultados
8. Commit: `refactor: migrate Pydantic schemas from class Config to model_config ConfigDict`

**Rollback:** Revert del commit — cambio atómico y seguro.