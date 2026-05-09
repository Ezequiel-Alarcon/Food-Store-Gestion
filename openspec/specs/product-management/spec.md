# Product Management Specification

## Overview

CRUD completo para la gestión de productos del catálogo, incluyendo gestión de stock y asociaciones con categorías e ingredientes.

## Functionality

### 1. Create Product (US-015)

**Endpoint**: `POST /api/v1/productos`

**Authorization**: ADMIN, GESTOR_STOCK

**Request Body**:
```json
{
  "nombre": "string (required, max 200)",
  "descripcion": "string (optional, max 2000)",
  "precio": "decimal > 0 (required)",
  "imagen_url": "string (optional, URL)",
  "stock": "integer >= 0 (required, default 0)",
  "categoria_ids": "array of integers (optional)",
  "ingrediente_ids": "array of integers (optional)",
  "activo": "boolean (optional, default true)"
}
```

**Response**: 201 Created con el producto creado

**Rules**:
- RN-ST01: El precio debe ser mayor a 0
- RN-ST02: El stock inicial no puede ser negativo

### 2. List Products (Admin) (US-016)

**Endpoint**: `GET /api/v1/productos`

**Authorization**: ADMIN, GESTOR_STOCK

**Query Parameters**:
- `skip`: integer (default 0)
- `limit`: integer (default 20, max 100)
- `categoria_id`: integer (optional, filter by category)
- `activo`: boolean (optional, filter by status)

**Response**: 200 OK con paginación

### 3. Get Product Detail (US-019)

**Endpoint**: `GET /api/v1/productos/{producto_id}`

**Authorization**: ADMIN, GESTOR_STOCK

**Response**: 200 OK con el producto incluyendo categorías e ingredientes asociados

### 4. Update Product (US-020)

**Endpoint**: `PUT /api/v1/productos/{producto_id}`

**Authorization**: ADMIN, GESTOR_STOCK

**Request Body**: Mismos campos que Create (todos opcionales)

**Response**: 200 OK con el producto actualizado

**Rules**:
- RN-ST03: No se puede editar un producto marcado como eliminado (soft-delete)

### 5. Manage Stock (US-021)

**Endpoint**: `PATCH /api/v1/productos/{producto_id}/stock`

**Authorization**: ADMIN, GESTOR_STOCK

**Request Body**:
```json
{
  "stock": "integer >= 0 (required)",
  "operacion": "enum: 'set', 'add', 'subtract'"
}
```

**Response**: 200 OK con el nuevo stock

**Rules**:
- RN-ST04: Si operacion es 'subtract', el stock no puede quedar negativo

### 6. Delete Product (Soft-Delete) (US-022)

**Endpoint**: `DELETE /api/v1/productos/{producto_id}`

**Authorization**: ADMIN

**Response**: 204 No Content

**Rules**:
- RN-ST05: El producto no se elimina físicamente, se marca como eliminado (soft-delete)
- RN-ST06: Un producto eliminado no aparece en el catálogo público

## Data Model

### Producto Entity
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PK, auto-increment |
| nombre | String | max 200, not null |
| descripcion | String | max 2000, nullable |
| precio | Decimal | > 0, not null |
| imagen_url | String | nullable |
| stock | Integer | >= 0, default 0 |
| activo | Boolean | default true |
| eliminado_en | DateTime | nullable (soft-delete) |
| creado_en | DateTime | auto |
| actualizado_en | DateTime | auto |

### ProductoCategoria (Join Table)
| Field | Type |
|-------|------|
| producto_id | FK Producto |
| categoria_id | FK Categoria |

### ProductoIngrediente (Join Table)
| Field | Type |
|-------|------|
| producto_id | FK Producto |
| ingrediente_id | FK Ingrediente |

## Error Handling

- 404: Producto no encontrado
- 400: Validación de datos (precio <= 0, stock negativo)
- 409: Conflicto (producto eliminado)

## Acceptance Criteria

- [x] Un ADMIN puede crear productos con nombre, precio, stock, categorías e ingredientes
- [x] Un GESTOR_STOCK puede crear productos pero no eliminar
- [x] El stock se puede modificar independientemente del producto
- [x] La eliminación es soft-delete (no físico)
- [x] Los productos eliminados no aparecen en listados públicos