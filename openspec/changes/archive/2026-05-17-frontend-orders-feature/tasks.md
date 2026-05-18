# Tasks: frontend-orders-feature

- [ ] 1. Mover `pages/OrdersPage.tsx` → `features/orders/OrdersPage.tsx`
- [ ] 2. Corregir import path interno: `../entities/pedido` → `../../entities/pedido`
- [ ] 3. Crear `features/orders/index.ts` barrel export
- [ ] 4. Eliminar `features/orders/.gitkeep`
- [ ] 5. Actualizar import en `providers/RouterProvider.tsx`: `'../pages/OrdersPage'` → `'../features/orders'`
- [ ] 6. Verificar que no queden referencias huérfanas a `pages/OrdersPage`
