## Why

Verificación manual post `auth-audit` reveló bugs en 4 módulos que impiden el funcionamiento correcto de endpoints. Los bugs críticos son errores 500 en categorías e ingredientes por SQLAlchemy `text()` en CTEs recursivas. Adicionalmente, productos no devuelve mensaje al eliminar, y categorías interpreta `0` como FK válida en updates.

## What Changes

- **Categorías**: Arreglar error 500 en `delete_categoria` y `get_subcategorias` — queries CTE usan raw SQL sin wrapper `text()` requerido por SQLAlchemy 2.0+
- **Categorías**: En `update_categoria`, `categoria_padre_id = 0` debe tratarse como "sin padre" (NULL), no como FK a ID 0
- **Ingredientes**: Arreglar error 500 en `delete_ingrediente` (probablemente mismo bug de `text()` o modelo roto)
- **Productos**: Agregar `response_model` o mensaje de confirmación en el endpoint de eliminación
- **Direcciones**: Revisar creación de sucursal sin dirección asociada (validación de FK)

## Capabilities

### Modified Capabilities
- `category-crud`: Arreglar queries CTE con `text()`, arreglar update con `categoria_padre_id = 0`
- `category-hierarchy`: Arreglar `get_subcategorias` con `text()` en CTE recursiva
- `ingredient-crud`: Arreglar delete de ingrediente (error 500)
- `product-management`: Agregar mensaje de confirmación en delete
- `branch-addresses`: Revisar creación de sucursal sin dirección

## Impact

- **Archivos modificados**: `categorias/repository.py`, `categorias/router.py`, `categorias/service.py`, `ingredientes/repository.py`, `productos/router.py`, `sucursales/router.py`
- **Frontend**: sin impacto
- **Breaking**: ninguno
