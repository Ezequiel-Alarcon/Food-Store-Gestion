# Spec: admin-categories-crud

> **Rol:** ADMIN  
> **Ruta:** `/admin/categorias`

## Requisitos

### RQ-CAT01 — Listado de categorías
- `GET /api/v1/categorias` — listado con jerarquía (CTE recursiva)
- Tabla con columnas: Nombre, Categoría Padre, Estado (activa/inactiva), Acciones
- Indentación visual para mostrar jerarquía (categorías hijas con padding-left)
- Loading skeleton

### RQ-CAT02 — Crear categoría
- `POST /api/v1/categorias` — body: `{ nombre, categoria_padre_id? }`
- Modal con: campo nombre (requerido), select de categoría padre (opcional)
- Toast de éxito/error
- Refetch del listado al crear

### RQ-CAT03 — Editar categoría
- `PUT /api/v1/categorias/{id}` — body: `{ nombre, categoria_padre_id? }`
- Mismo modal que crear, precargado con datos actuales

### RQ-CAT04 — Eliminar categoría
- `DELETE /api/v1/categorias/{id}` — soft-delete
- Confirmación modal antes de eliminar
- Toast de confirmación

## Escenarios

```
GIVEN usuario ADMIN autenticado
WHEN navega a /admin/categorias
THEN ve tabla con todas las categorías y su jerarquía
WHEN hace clic en "Nueva categoría"
AND completa nombre "Bebidas" y padre "null"
AND guarda
THEN categoría aparece en la tabla
```
