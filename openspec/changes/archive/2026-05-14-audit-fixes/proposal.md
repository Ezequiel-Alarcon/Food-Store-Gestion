## Why

Auditoría exhaustiva del frontend encontró 2 bugs críticos y múltiples warnings que degradan la UX. Los roles del backend (`STOCK`, `PEDIDOS`) no matchean con los del frontend (`GESTOR_STOCK`, `GESTOR_PEDIDOS`), y el código de estado `EN_PREP` del backend no coincide con `EN_PREPARACION` del frontend. Además hay issues de navegación, modales, y consistencia.

## What Changes

- Sincronizar roles: `GESTOR_STOCK`→`STOCK`, `GESTOR_PEDIDOS`→`PEDIDOS` en Navigation y RouterProvider
- Corregir estado `EN_PREPARACION`→`EN_PREP` en OrdersPage
- Links login/register: `<a>`→`<Link>` para evitar full reload
- ConfirmModal: try/finally para que cierre aunque falle onConfirm
- CartSummary: eliminar altura hardcodeada
- Badge detalle pedido: mismo fallback que la tabla
- Usar `totalPrice()` del cartStore en vez de calcular manual
- Limpiar error al abrir detalle en OrdersPage

## Impact

- Navigation.tsx, RouterProvider.tsx, OrdersPage.tsx, CartSummary.tsx, CartPage.tsx, ConfirmModal.tsx, RegisterForm.tsx, LoginForm.tsx
