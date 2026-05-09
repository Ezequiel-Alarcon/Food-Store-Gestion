## Why

Sin el módulo de productos, el e-commerce no tiene nada que vender. Los clientes no pueden navegar el catálogo, los gestores de stock no pueden gestionar inventario, y el proceso de pedidos no puede existir. Es el corazón del sistema de ventas.

## What Changes

- **Nuevo módulo `productos`** en backend: model, schemas, repository, service, router
- **CRUD completo**: crear, listar, editar, eliminar (soft-delete) productos
- **Gestión de stock**: actualizar cantidad disponible por producto
- **Asociación categorías**: cada producto puede pertenecer a múltiples categorías (relación muchos-a-muchos)
- **Asociación ingredientes**: cada producto puede contener múltiples ingredientes (relación muchos-a-muchos)
- **Catálogo público**: endpoint sin auth para listar productos disponibles
- **Filtros por alérgenos**: endpoint para filtrar productos que NO contengan ciertos ingredientes/alérgenos
- **Relación con cambios anteriores**: depende de `categories-module` (8) e `ingredients-module` (9) ya implementados

## Capabilities

### New Capabilities

- `product-management`: CRUD completo de productos con gestión de stock
- `product-catalog`: Catálogo público con filtros por categoría y alérgenos

### Modified Capabilities

- Ninguna. Los módulos de categorías e ingredientes ya existen y no requieren cambios en sus specs.

## Impact

- **Backend**: Nuevo módulo `app/modules/productos/` con ~10 archivos
- **API**: Nuevos endpoints bajo `/api/v1/productos/`
- **Dependencias**: Requiere que categories (8) e ingredients (9) estén mergeados a main
- **Frontend futuro**: Este change es solo backend; el frontend de productos se implementará en change separado (cart-frontend depends on it)