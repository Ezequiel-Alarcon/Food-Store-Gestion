# Proposal: admin-catalog-ui

## Why

El panel de administración carece de UI para gestionar el catálogo: no se pueden crear/editar/eliminar categorías ni productos desde el frontend, y los badges de alérgenos no se muestran en la vista de ingredientes. El backend tiene todos los endpoints implementados y funcionales — solo falta el frontend. Para la demo en video, el admin debe poder mostrar gestión completa del catálogo.

## What Changes

- **Categorías CRUD:** Página de gestión de categorías jerárquicas con tabla tree, crear/editar/eliminar, visualización de jerarquía (CTE recursiva).
- **Productos CRUD:** Página de gestión de productos con formulario de creación/edición (nombre, precio, descripción, imagen, categorías, ingredientes), listado con filtros, soft-delete.
- **Badges de alérgenos:** Agregar campo `es_alergeno` al tipo `IngredienteSimple` en frontend y mostrar badge visual (⚠️) en IngredientsModal y vistas de producto.

## Capabilities

### New Capabilities

- `admin-categories-crud`: Interfaz CRUD de categorías jerárquicas para ADMIN.
- `admin-products-crud`: Interfaz CRUD de productos con relaciones (categorías, ingredientes) para ADMIN.
- `allergen-badges-ui`: Visualización de badges de alérgenos en ingredientes.

### Modified Capabilities

Ninguna. Los endpoints del backend no cambian.

## Impact

- **Archivos:** ~8 nuevos/creados en `features/admin/categories/`, `features/admin/products/`, `entities/producto/types.ts`
- **Riesgo:** Medio — formularios complejos con relaciones N:M (producto↔categoría, producto↔ingrediente)
- **Dependencias:** Backend con endpoints de categorías y productos ya implementados
