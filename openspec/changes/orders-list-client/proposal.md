## Why

El backend de pedidos (`orders-fsm`) está completo y expone endpoints para listar y ver detalle de pedidos. El frontend actualmente tiene un placeholder en `/pedidos`. El cliente necesita ver sus pedidos con estado, total y fecha, y poder acceder al detalle de cada uno.

## What Changes

- Crear `entities/pedido/` con types y API client
- Crear `pages/OrdersPage.tsx` con lista de pedidos paginada, filtro por estado
- Crear modal/drawer de detalle de pedido (items, dirección, total)
- Reemplazar placeholder en RouterProvider por OrdersPage

## Capabilities

### New Capabilities
- `client-orders`: Página de mis pedidos con listado paginado, filtro por estado, y detalle de pedido

## Impact

- `frontend/src/entities/pedido/` (nuevo)
- `frontend/src/pages/OrdersPage.tsx` (nuevo)
- `frontend/src/providers/RouterProvider.tsx` (modificado)
