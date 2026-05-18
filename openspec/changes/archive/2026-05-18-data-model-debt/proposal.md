# Proposal: data-model-debt

## Why

La auditoría spec vs código reveló 4 desviaciones en el modelo de datos que la spec SDD v5.0 requiere pero el código no implementa: `es_principal` en ProductoCategoria, `es_removible` en ProductoIngrediente, soft-delete consistente en Categoria (`eliminado_en` vs `activa`), y `unique` en Ingrediente.nombre. Son cambios pequeños pero necesarios para completitud del ERD v5.

## What Changes

- **ProductoCategoria + `es_principal`:** Agregar campo `es_principal: bool = False` a la tabla pivot. Permite marcar una categoría como principal para un producto.
- **ProductoIngrediente + `es_removible`:** Agregar campo `es_removible: bool = False`. Habilita la personalización de pedidos (qué ingredientes se pueden excluir).
- **Categoria `activa` → `eliminado_en`:** Migrar de booleano a timestamp soft-delete, consistente con el resto de entidades (Producto, Usuario).
- **Ingrediente `nombre` unique:** Agregar constraint `unique=True` y validación en servicio para evitar duplicados.

## Capabilities

### Modified Capabilities

Ninguna. Cambios internos de modelo — no modifican comportamiento de specs existentes.

## Impact

- **Archivos:** `productos/model.py`, `categorias/model.py`, `ingredientes/model.py`, `categorias/service.py`, `ingredientes/service.py`
- **Migración:** 1 nueva migración Alembic
- **Riesgo:** Medio — migración de esquema con datos existentes
- **Dependencias:** Ninguna
