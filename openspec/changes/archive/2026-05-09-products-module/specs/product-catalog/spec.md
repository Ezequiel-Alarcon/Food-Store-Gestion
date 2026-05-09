# Product Catalog Specification

## Overview

Catálogo público de productos para clientes, con filtros por categoría y alérgenos.

## Functionality

### 1. Public Catalog (US-018)

**Endpoint**: `GET /api/v1/productos/catalogo`

**Authorization**: None (public)

**Query Parameters**:
- `skip`: integer (default 0)
- `limit`: integer (default 20, max 100)
- `categoria_id`: integer (optional, filter by category)
- `disponibles`: boolean (optional, filter by stock > 0)

**Response**: 200 OK con paginación

**Rules**:
- RN-CT01: Solo devuelve productos con `activo = true` y `eliminado_en = null`
- RN-CT02: No muestra productos con stock = 0 a menos que se pida explícitamente

### 2. Filter by Allergens (US-023)

**Endpoint**: `GET /api/v1/productos/catalogo`

**Query Parameters adicionales**:
- `excluir_alergenos`: boolean (optional, default false)
- `ingrediente_ids`: string (optional, comma-separated IDs to exclude)

**Examples**:
- `GET /catalogo?excluir_alergenos=true` → exclude products with any allergen ingredient
- `GET /catalogo?ingrediente_ids=1,3,5` → exclude products containing ingredients 1, 3, or 5

**Rules**:
- RN-CT03: Si `excluir_alergenos=true`, exclude productos que contengan ingredientes con `es_alergeno = true`
- RN-CT04: La exclusión de ingredientes es acumulativa con la de alérgenos

### 3. Product Detail (Public) (US-019)

**Endpoint**: `GET /api/v1/productos/{producto_id}/publico`

**Authorization**: None (public)

**Response**: 200 OK con el producto (sin datos sensibles como stock exacto)

**Rules**:
- RN-CT05: Si el producto está eliminado o inactivo, devuelve 404
- RN-CT06: No revela el stock exacto, solo si está disponible o no

## Data Model

El catálogo utiliza las mismas entidades de Product Management, más la relación con Ingrediente.es_alergeno.

## Error Handling

- 404: Producto no encontrado o no disponible
- 400: Parámetros de filtro inválidos

## Acceptance Criteria

- [ ] El catálogo público es accesible sin autenticación
- [ ] Los productos eliminados/inactivos no aparecen en el catálogo
- [ ] Se puede filtrar por categoría
- [ ] Se puede excluir productos con alérgenos
- [ ] Se puede excluir productos por ingredientes específicos
- [ ] El detalle público no revela stock exacto