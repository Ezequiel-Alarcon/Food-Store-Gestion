## 1. API Client

- [x] 1.1 Crear `frontend/src/entities/pedido-admin/api.ts` — cliente API para endpoints admin (list, getById)
- [x] 1.2 Crear tipos en `frontend/src/entities/pedido-admin/types.ts` — interfaces para OrderAdmin, OrderDetailAdmin

## 2. Orders List Page

- [x] 2.1 Crear `frontend/src/features/admin/orders/ui/OrdersListPage.tsx` — página principal
- [x] 2.2 Tabla integrada en OrdersListPage — columnas: ID, Cliente, Fecha, Estado, Total, Acciones
- [x] 2.3 Crear componente `StatusFilter.tsx` — dropdown para filtrar por estado
- [x] 2.4 Crear componente `ClientSearch.tsx` — input de búsqueda por nombre de cliente
- [x] 2.5 Paginación implementada en OrdersListPage
- [x] 2.6 Skeleton loaders implementados

## 3. Order Detail Page

- [x] 3.1 Crear `frontend/src/features/admin/orders/ui/OrderDetailPage.tsx` — página de detalle
- [x] 3.2 Componente OrderInfoCard integrado en OrderDetailPage
- [x] 3.3 Componente OrderItemsList integrado en OrderDetailPage
- [x] 3.4 Componente OrderTimeline integrado en OrderDetailPage
- [x] 3.5 Componente OrderAddressCard integrado en OrderDetailPage
- [x] 3.6 Payment info integrada en OrderInfoCard

## 4. Routing & Navigation

- [x] 4.1 Ruta `/admin/pedidos` en RouterProvider.tsx
- [x] 4.2 Ruta `/admin/pedidos/:id` en router
- [x] 4.3 Menú de navegación actualizado — "Gestión de Pedidos" para ADMIN
- [x] 4.4 Rutas protegidas con ProtectedRoute (roles: PEDIDOS, ADMIN)

## 5. Testing

- [ ] 5.1 Verificar que la página carga correctamente
- [ ] 5.2 Verificar filtros funcionan (estado, búsqueda)
- [ ] 5.3 Verificar navegación a detalle
- [ ] 5.4 Verificar timeline muestra todas las transiciones