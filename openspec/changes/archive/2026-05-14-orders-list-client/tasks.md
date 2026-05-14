## 1. Entidad Pedido

- [x] 1.1 Crear `entities/pedido/types.ts` — interfaces: `PedidoListItem`, `PedidoDetalle`, `DetalleItem`, `PaginatedPedidos`
- [x] 1.2 Crear `entities/pedido/api.ts` — `getMisPedidos(params)` y `getPedidoById(id)`
- [x] 1.3 Crear `entities/pedido/index.ts` — barrel export

## 2. Página de Pedidos

- [x] 2.1 Crear `pages/OrdersPage.tsx` — lista de pedidos con fetch, paginación, filtro por estado, loading/empty/error
- [x] 2.2 Crear badge de estado con colores según estado del pedido
- [x] 2.3 Crear drawer/modal de detalle de pedido (items, dirección, total)

## 3. Integración

- [x] 3.1 Reemplazar placeholder en `RouterProvider.tsx` por `<OrdersPage />`
