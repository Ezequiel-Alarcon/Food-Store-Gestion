## Context

Verificación manual de endpoints post `auth-audit`. Bugs encontrados en módulos de categorías, ingredientes, productos y direcciones.

## Goals / Non-Goals

**Goals:**
- Arreglar error 500 en queries CTE de categorías (agregar wrapper `text()`)
- Arreglar `categoria_padre_id = 0` que se confunde con FK
- Arreglar delete de ingrediente (mismo patrón `text()`)
- Agregar mensaje de confirmación en delete de producto
- Revisar validación de sucursal sin dirección

**Non-Goals:**
- Pagos y admin (marcados PENDIENTE por el usuario, scope separado)
- Refactors de arquitectura

## Decisions

### D1: Wrappear raw SQL CTE con `text()`
SQLAlchemy 2.0+ requiere que queries SQL textuales se pasen como `text("...")`. Las queries CTE en `categorias/repository.py` usan f-strings crudos. Fix: `from sqlalchemy import text` + wrappear.

### D2: `categoria_padre_id = 0` → NULL
El schema recibe `0` del frontend como "sin padre". En el service, convertir `0` a `None` antes de asignar al modelo.
