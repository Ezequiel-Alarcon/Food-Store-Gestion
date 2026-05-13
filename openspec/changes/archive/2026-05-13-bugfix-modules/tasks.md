## 1. Categorías — SQLAlchemy text() en CTE

- [x] 1.1 Agregar `from sqlalchemy import text` en `categorias/repository.py`
- [x] 1.2 Wrappear query CTE en `get_descendants_cte()` con `text()` y bound parameters
- [x] 1.3 Verificar que `delete_categoria` y `get_subcategorias` funcionan sin error 500

## 2. Categorías — categoria_padre_id = 0

- [x] 2.1 En `categorias/service.py`, convertir `categoria_padre_id = 0` a `None` en `update_categoria()`
- [x] 2.2 Verificar que actualizar categoría sin padre funciona correctamente

## 3. Ingredientes — Delete error 500

- [x] 3.1 Diagnosticar — el error era del CTE de categorías (mismo bug), no de ingredientes
- [x] 3.2 Verificar que eliminar ingrediente funciona correctamente (no requiere fix adicional)

## 4. Productos — Mensaje en delete

- [x] 4.1 Agregar `response_model=MessageResponse` en `DELETE /productos/{id}`
- [x] 4.2 Cambiar status de 204 a 200 con mensaje "Producto eliminado correctamente"

## 5. Direcciones — Sucursal sin dirección

- [x] 5.1 Revisar — la creación de sucursal no incluye dirección por diseño (endpoint separado)
- [x] 5.2 Sin cambios necesarios en este scope
