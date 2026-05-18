# Spec: stock-management-ui

> **Tipo:** Nueva capability (frontend)  
> **Cambio padre:** `mvp-critical-fixes`  
> **Rol:** STOCK, ADMIN

## Descripción

Interfaz de gestión de stock accesible desde `/admin/stock`. Permite al rol STOCK (y ADMIN) visualizar todos los productos con su stock actual, modificar cantidades, y alternar disponibilidad.

## Requisitos

### RQ-SM01 — Listado de productos con stock
- **GET /api/v1/productos** (admin, requiere auth)
- Mostrar tabla con columnas: nombre, stock actual, input de cantidad, toggle activo/disable
- Paginación
- Loading skeleton mientras carga

### RQ-SM02 — Edición de stock
- **PATCH /api/v1/productos/{id}/stock** con body `{stock: int, activo: bool}`
- Input numérico con botón Guardar por fila
- Feedback: toast verde (éxito) o rojo (error)
- Validación: stock ≥ 0

### RQ-SM03 — Toggle de disponibilidad
- Checkbox o switch por producto para `activo: true/false`
- Guardado inmediato al cambiar (sin botón extra)

### RQ-SM04 — Roles
- Acceso: `require_role("STOCK", "ADMIN")` en la ruta
- Admin ve todas las columnas, STOCK solo ve stock y activo (no precio, no categorías)

## Escenarios

### Escenario 1: STOCK actualiza cantidad
```
GIVEN usuario autenticado con rol STOCK
WHEN navega a /admin/stock
THEN ve tabla con todos los productos, stock actual, y campo de edición
WHEN cambia el valor de stock de "Hamburguesa" de 10 a 25
AND hace clic en Guardar
THEN se llama PATCH /productos/{id}/stock con {stock: 25, activo: true}
AND se muestra toast "Stock actualizado"
AND la tabla refleja el nuevo valor
```

### Escenario 2: ADMIN desactiva producto
```
GIVEN usuario autenticado con rol ADMIN
WHEN desmarca el toggle "Activo" de un producto
THEN se llama PATCH /productos/{id}/stock con {stock: current, activo: false}
AND el producto deja de aparecer en el catálogo público
```

## Archivos

- `frontend/src/features/admin/stock/StockManagementPage.tsx` — Componente principal
- `frontend/src/features/admin/stock/index.ts` — Barrel export
- `frontend/src/providers/RouterProvider.tsx` — Reemplazar placeholder por el componente
