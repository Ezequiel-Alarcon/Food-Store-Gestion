## Context

Python 3.12 deprecó `datetime.utcnow()` porque retorna un naive datetime que se interpreta como UTC por convención, pero Python no lo sabe — esto causa bugs sutiles en comparaciones con timezone-aware datetimes.

El fix es mecánico: buscar y reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en 21 lugares分布 across 4 archivos.

## Goals / Non-Goals

**Goals:**
- Eliminar todos los usages de `datetime.utcnow()` en código de producción
- Asegurar imports correctos de `timezone` donde sea necesario
- No alterar comportamiento de negocio — solo dependiente del tiempo

**Non-Goals:**
- No modificar tests (pueden usar `utcnow()` para setup de fixtures — son mocks)
- No modificar archivos en `.agents/skills/` (son templates de skill, no producción)
- No crear migración de DB — los existing timestamps en DB son UTC por convención

## Decisions

### Decision 1: Reemplazo mecánico con grep/sed

**Elección:** Reemplazo directo `datetime.utcnow()` → `datetime.now(timezone.utc)` archivo por archivo.

**Alternativas:**
- Usar un script de migración automatizado: overkill para 21 usages en 4 archivos
- Refactor a una helper function `utc_now()`: introduce indirección innecesaria

**Rationale:** Cambio simple y trazable con grep — cada occurrence es visible y auditable.

### Decision 2: Import de `timezone`

**Elección:** Agregar `timezone` al import de `datetime` existente en cada archivo.

**Rationale:** Mantiene el padrão actual de `from datetime import datetime, timezone`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Olvidar algún usage | Verificar con grep post-reemplazo que no quedan `utcnow()` en `app/` |
| Romper tests que usan `utcnow()` | Solo reemplazar en `app/modules/` — tests están en `tests/` |

## Migration Plan

1. Reemplazar en `backend/app/modules/productos/service.py` (2 usages)
2. Reemplazar en `backend/app/modules/productos/repository.py` (6 usages)
3. Reemplazar en `backend/app/modules/sucursales/service.py` (3 usages)
4. Reemplazar en `backend/app/modules/direcciones/service.py` (10 usages)
5. Verificar: `grep -r "utcnow" backend/app/modules/` debe retornar 0 resultados
6. Commit con mensaje: `fix: replace datetime.utcnow() with datetime.now(timezone.utc)`

**Rollback:** Revert del commit — cambio atómico y seguro.