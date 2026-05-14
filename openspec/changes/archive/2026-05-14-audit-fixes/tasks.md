## 1. Roles: STOCK/PEDIDOS

- [x] 1.1 Navigation.tsx: cambiar `GESTOR_STOCK`→`STOCK`, `GESTOR_PEDIDOS`→`PEDIDOS` en MENU_BY_ROLE
- [x] 1.2 RouterProvider.tsx: cambiar `GESTOR_STOCK`→`STOCK`, `GESTOR_PEDIDOS`→`PEDIDOS` en allowedRoles

## 2. Estado: EN_PREP

- [x] 2.1 OrdersPage.tsx: cambiar `EN_PREPARACION`→`EN_PREP` en ESTADOS, ESTADO_COLORS, ESTADO_LABELS

## 3. Navegación

- [x] 3.1 RegisterForm.tsx: `<a href="/login">`→`<Link to="/login">`
- [x] 3.2 LoginForm.tsx: `<a href="/register">`→`<Link to="/register">`

## 4. Modales y UI

- [x] 4.1 ConfirmModal.tsx: try/finally en handleConfirm para que cierre siempre
- [x] 4.2 CartSummary.tsx: eliminar `h-[calc(100%-49px)]`, usar `flex-1`
- [x] 4.3 OrdersPage.tsx: badge fallback consistente en drawer de detalle
- [x] 4.4 OrdersPage.tsx: limpiar error al abrir detalle (setError(null))

## 5. DRY

- [x] 5.1 CartPage.tsx + CartSummary.tsx: usar `totalPrice()` del cartStore en vez de calcular manual
