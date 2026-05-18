# Design: admin-catalog-ui

## Context

El backend tiene endpoints CRUD completos para categorías (`/api/v1/categorias`) y productos (`/api/v1/productos`). El frontend solo tiene vista pública de catálogo (`CatalogPage`). El panel admin necesita UI para gestionar ambas entidades.

## Goals / Non-Goals

**Goals:**
- ADMIN puede crear, editar y eliminar categorías jerárquicas desde UI
- ADMIN puede crear, editar, soft-delete productos con sus relaciones desde UI
- Los badges de alérgenos se muestran en IngredientsModal y vistas de producto

**Non-Goals:**
- NO modificar backend
- NO modificar la vista pública de catálogo
- NO implementar drag & drop para jerarquía de categorías (solo select de padre)

## Decisions

### Categorías — Tabla tree con CRUD

**Endpoints usados:**
- `GET /api/v1/categorias` — listado plano o tree
- `POST /api/v1/categorias` — crear (requiere `nombre`, opcional `categoria_padre_id`)
- `PUT /api/v1/categorias/{id}` — editar
- `DELETE /api/v1/categorias/{id}` — soft-delete

**UI:** Tabla con columnas: Nombre, Padre, Acciones (Editar, Eliminar). Modal para crear/editar con campo nombre + select de categoría padre.

### Productos — Formulario CRUD con relaciones

**Endpoints usados:**
- `GET /api/v1/productos` (admin) — listado con stock
- `POST /api/v1/productos` — crear con `categoria_ids`, `ingrediente_ids`
- `PUT /api/v1/productos/{id}` — editar
- `DELETE /api/v1/productos/{id}` — soft-delete

**UI:** Página con tabla de productos + botón "Nuevo producto". Modal/formulario con campos: nombre, descripción, precio, imagen_url, categorías (multi-select checkboxes), ingredientes (multi-select checkboxes con badge de alérgenos).

### Badges de alérgenos

**Cambio:** Agregar `es_alergeno: boolean` al tipo `IngredienteSimple` en `entities/producto/types.ts`. En `IngredientsModal.tsx`, mostrar ⚠️ o badge rojo junto al nombre del ingrediente si `es_alergeno === true`.

## Risks / Trade-offs

- **Formulario de producto complejo:** Relaciones N:M con categorías e ingredientes requieren dos multi-selects. → Mantener simple: checkboxes con scroll.
- **Jerarquía de categorías:** CTE recursiva del backend devuelve estructura plana. → Mostrar indentación visual según nivel de profundidad.
