# Spec: admin-products-crud

> **Rol:** ADMIN  
> **Ruta:** `/admin/productos`

## Requisitos

### RQ-PROD01 — Listado de productos (admin)
- `GET /api/v1/productos` (admin) — listado completo con stock
- Tabla: Nombre, Precio, Stock, Activo, Acciones (Editar, Eliminar)
- Paginación
- Botón "Nuevo producto"

### RQ-PROD02 — Crear producto
- `POST /api/v1/productos` — body con `nombre, descripcion?, precio, imagen_url?, categoria_ids[], ingrediente_ids[]`
- Formulario en modal/página con:
  - Nombre (input, requerido)
  - Descripción (textarea, opcional)
  - Precio (input numérico, requerido, > 0)
  - Imagen URL (input, opcional)
  - Categorías (checkboxes, multi-select)
  - Ingredientes (checkboxes con badge de alérgenos ⚠️)
- Validación client-side + toast éxito/error

### RQ-PROD03 — Editar producto
- `PUT /api/v1/productos/{id}`
- Mismo formulario que crear, precargado

### RQ-PROD04 — Eliminar producto
- `DELETE /api/v1/productos/{id}` — soft-delete
- Confirmación modal

## Escenarios

```
GIVEN usuario ADMIN
WHEN navega a /admin/productos
AND hace clic en "Nuevo producto"
AND completa nombre "Hamburguesa Clásica", precio 1500
AND selecciona categoría "Hamburguesas" e ingredientes "Pan, Carne, Lechuga"
AND guarda
THEN producto aparece en la tabla
```
