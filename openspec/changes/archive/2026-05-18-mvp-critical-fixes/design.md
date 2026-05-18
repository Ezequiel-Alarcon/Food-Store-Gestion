# Design: mvp-critical-fixes

## Context

El proyecto está a horas de la demo en video. La auditoría encontró 4 bugs que bloquean funcionalidad visible: checkout roto, FSM inoperable, stock placeholder, logout inseguro. Los endpoints del backend funcionan correctamente — el problema está en el frontend.

## Goals / Non-Goals

**Goals:**
- Flujo de checkout funcional end-to-end (carrito → dirección → pago → confirmación)
- Admin/PEDIDOS puede avanzar/cancelar estados de pedidos desde la UI
- STOCK puede ver y editar cantidades de productos desde el panel
- Logout revoca refresh token en el backend

**Non-Goals:**
- NO modificar backend
- NO agregar nuevos endpoints
- NO modificar specs
- NO hacer refactors de arquitectura

## Decisions

### Fix 1: Checkout Flow — Cart cleared AFTER payment

**Problema actual:** `CartPage.tsx:41` llama `clearCart()` antes de `navigate('/checkout?pedido=X')`. `CheckoutPage.tsx:36-40` detecta `items.length === 0` y redirige a `/productos`.

**Solución:**
1. `CartPage` NO limpia el carrito al navegar a checkout
2. `CheckoutPage` carga datos del pedido desde el backend (`GET /api/v1/pedidos/{pedidoId}`) en vez de depender de `cartStore.items`
3. El carrito se limpia SOLO en step 4 (`approved`), en `PaymentResult.tsx` o `paymentStore`

**Trade-off:** CheckoutPage ahora hace una request extra al backend para obtener los datos del pedido, pero es más robusto (no depende del carrito local).

### Fix 2: FSM Transitions UI — Botones en OrderDetailPage

**Problema actual:** `OrderDetailPage.tsx` muestra datos del pedido pero sin controles de transición.

**Solución:** Agregar `StateTransition` component que:
1. Lee `estado_codigo` del pedido y `TRANSICIONES_VALIDAS` de la FSM
2. Muestra botones solo para transiciones permitidas (según estado + rol)
3. Si destino es CANCELADO → muestra input para motivo (RN-05)
4. Llama `PATCH /api/v1/pedidos/{id}/estado` con TanStack Query `useMutation`

### Fix 3: Stock Management — Página real con TanStack Query

**Problema actual:** Ruta `/admin/stock` renderiza un `<div>` placeholder.

**Solución:** Crear `StockManagementPage.tsx` en `features/admin/stock/`:
1. `useQuery` → `GET /api/v1/productos` (admin, con stock)
2. Tabla con columnas: nombre, stock actual, input para nuevo stock, toggle activo
3. `useMutation` → `PATCH /api/v1/productos/{id}/stock` para guardar cambios
4. Feedback visual: toast de éxito/error, optimistic update

### Fix 4: Logout Seguro — Llamada al backend

**Problema actual:** `authStore.logout()` solo limpia estado local.

**Solución:**
1. Antes de `set()` para limpiar, llamar `api.post('/auth/logout', { refresh_token: get().refreshToken })`
2. Envolver en try/catch — si falla (token ya revocado, red), limpiar estado local igual
3. Redirigir a `/login` al terminar

## Risks / Trade-offs

- **Fix 1:** Si el backend no devuelve datos del pedido rápido, CheckoutPage muestra loading → Mitigación: mostrar skeleton loader mientras carga
- **Fix 2:** El rol se obtiene del authStore (single rol). Si el usuario tiene múltiples roles, puede no ver todos los botones → Mitigación aceptable para MVP
- **Fix 3:** La tabla usa optimistic updates. Si el PATCH falla, hay que hacer rollback → Implementar `onError` en useMutation con invalidación de queries
- **Fix 4:** Si el backend no responde, el logout local procede igual → UX no bloqueante
