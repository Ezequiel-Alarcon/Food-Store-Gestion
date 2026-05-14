# Tasks: checkout-frontend

## 1. Backend Fixes (CRITICAL — must be done first)

- [x] 1. **Add `token` field to `PagoCreate` schema** — `backend/app/modules/pagos/schemas.py`: add `token: Optional[str] = None` import from `typing` and field with docstring on `PagoCreate`. No other fields changed.
  - Satisfies: REQ-CP03

- [x] 2. **Pass `token` to MercadoPago SDK in `crear_pago` service** — `backend/app/modules/pagos/service.py` ~line 198: after building `payment_data` dict and before `sdk.payment().create()`, add conditional `if data.token: payment_data["token"] = data.token`. Do NOT modify `reintentar_pago`.
  - Satisfies: REQ-CP03

## 2. Entity: pago (frontend entities layer)

- [x] 3. **Create `entities/pago/types.ts`** — TypeScript interfaces: `PagoCreateRequest` (`pedido_id`, `payment_method_id`, `token?`), `PagoResponse` (id, pedido_id, mp_payment_id, idempotency_key, external_reference, status, status_detail, payment_method_id, transaction_amount, created_at, updated_at), and `PagoStatus` union type (`'pending' | 'approved' | 'rejected' | 'in_process' | 'cancelled' | 'refunded'`).
  - Satisfies: REQ-CP01, REQ-CP03

- [x] 4. **Create `entities/pago/api.ts`** — Axios client with three methods: `create(payload: PagoCreateRequest): Promise<PagoResponse>` → `POST /pagos/crear`, `getByPedidoId(pedidoId: number): Promise<PagoResponse>` → `GET /pagos/{pedidoId}`, `retry(pedidoId: number): Promise<PagoResponse>` → `POST /pagos/{pedidoId}/reintentar`. Use existing `api` instance from `../../lib/api`.
  - Satisfies: REQ-CP03, REQ-CP04, REQ-CP06

- [x] 5. **Create `entities/pago/queries.ts`** — TanStack Query hooks: `useCreatePago` mutation, `usePagoStatus(pedidoId, enabled)` query with `refetchInterval` polling every 3s while status is `pending` or `in_process` (stop on `approved`, `rejected`, `cancelled`, `refunded`), and `useRetryPago` mutation that invalidates the pago query cache on success. Follow the same pattern as `entities/addresses/queries.ts`.
  - Satisfies: REQ-CP04, REQ-CP06, NFR-CP02

- [x] 6. **Create `entities/pago/index.ts`** — barrel re-exports: types, api, and queries hooks.

## 3. Page & Routing

- [x] 7. **Create `pages/CheckoutPage.tsx`** — Multi-step wizard orchestrator component. Extracts `pedido` from `searchParams`. Manages local state: `currentStep` (1-4), `selectedAddressId`, and `pagoResponse`. Step flow: 1=AddressSelector, 2=CheckoutSummary, 3=CardPaymentForm, 4=PaymentResult. Handles edge cases: missing pedido query param → redirect `/carrito` with toast, empty cart → redirect `/productos` with toast, pedido already paid → redirect `/pedidos/{id}`. Includes progress indicator (4 steps, clickable completed steps). Calls `usePaymentStore.resetPayment()` on unmount cleanup.
  - Satisfies: REQ-CP07, REQ-CP08, REQ-CP10

- [x] 8. **Register `/checkout` route in `RouterProvider.tsx`** — Wrap `<CheckoutPage />` in `<ProtectedRoute allowedRoles={['CLIENT']}>` at path `/checkout`. Add import for `CheckoutPage` alongside existing page imports.
  - Satisfies: REQ-CP01 (route access control)

## 4. Feature Components

- [x] 9. **Create `features/checkout/types.ts`** — Shared TypeScript types for the checkout feature: `CheckoutStep`, `AddressSelectorProps`, `CheckoutSummaryProps`, `CardPaymentFormProps`, `PaymentResultProps`. No logic, just types.
  - Satisfies: REQ-CP01, REQ-CP08

- [x] 10. **Create `features/checkout/AddressSelector.tsx`** — Step 1 component. Uses `useUserAddresses()` from `entities/addresses/queries`. Renders radio button list of saved addresses (shows calle, numero, ciudad, provincia). Pre-selects `is_default` address. Emits `onSelect(addressId)` callback. Handles loading (skeleton cards), empty (message + CTA button linking to `/direcciones`), and error (toast + retry button) states.
  - Satisfies: REQ-CP08

- [x] 11. **Create `features/checkout/CheckoutSummary.tsx`** — Step 2 component. Reads `items` from `useCartStore` and computes subtotal/total via `totalPrice()`. Shows item list (product name, qty, line total). Displays selected address summary from address query cache. Includes "Confirmar y pagar" button → advances to step 3. Handles edge case: cart empty → toast + redirect to `/carrito`.
  - Satisfies: REQ-CP10

- [x] 12. **Create `features/checkout/CardPaymentForm.tsx`** — Step 3 component. Wraps `<CardPayment>` from `@mercadopago/sdk-react`. Receives `pedidoId` and `amount` as props. On `onSubmit`, extracts `{token, payment_method_id}` from `formData` and calls `useCreatePago().mutateAsync()`. On success, passes `PagoResponse` to parent. On error, shows toast via `useUIStore.addToast()`. Disables Brick submit button while mutation is in-flight (via loading state). Handles Brick `onError` callback with toast. Wraps Brick in an `ErrorBoundary` for render failures.
  - Satisfies: REQ-CP01, REQ-CP02, REQ-CP03, REQ-CP09

- [x] 13. **Create `features/checkout/PaymentResult.tsx`** — Step 4 component. Receives `pagoResponse` and `pedidoId`. Renders success screen (green check, "¡Pago aprobado!", payment details: method, amount, installments, order #) with "Ver pedido" button → `/pedidos/{id}` and "Seguir comprando" → `/productos`. Renders rejected screen (red X, "Pago rechazado", human-readable explanation of `status_detail`, "Reintentar con otra tarjeta" button → back to step 3, "Cancelar" → `/pedidos/{id}`). Renders processing screen (spinner, "Procesando tu pago...") with `usePagoStatus` polling. Implements polling timeout (max 30 attempts / 90s) with fallback message and "Ver estado del pedido" button.
  - Satisfies: REQ-CP04, REQ-CP05, REQ-CP06, NFR-CP02

- [x] 14. **Create `features/checkout/index.ts`** — barrel exports for all four components and shared types.

## 5. MP SDK Initialization

- [x] 15. **Initialize MercadoPago SDK in `main.tsx`** — Add `import { initMercadoPago } from '@mercadopago/sdk-react'` and call `initMercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY, { locale: 'es-AR' })` BEFORE `createRoot(...).render(...)`. Add `VITE_MP_PUBLIC_KEY` to `.env.example` with placeholder value `TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
  - Satisfies: REQ-CP01, REQ-CP09

## 6. Integration

- [x] 16. **Wire "Finalizar pedido" from cart to create pedido → redirect to checkout** — In the cart page or cart feature component, add/create the "Finalizar pedido" button handler. On click: `POST /api/v1/pedidos` with cart items and selected address, then on 201 success redirect to `/checkout?pedido={id}`. If user has no addresses, show toast prompting to add one first. If cart empty, button is disabled. Must use the existing pedido API client pattern (check `entities/pedido/` for existing api and add `create` method if missing).
  - Satisfies: REQ-CP07

- [x] 17. **Connect checkout page to existing Zustand stores** — Integrate `usePaymentStore` (call `updatePaymentStatus` from polling results, `resetPayment` on unmount), `useCartStore` (read items for summary), and `useUIStore.addToast()` (all user-facing notifications). Update `usePaymentStore.startCheckout()` call in step 3 when entering payment flow.
  - Satisfies: NFR-CP04

- [x] 18. **Add navigation guards for checkout** — In `CheckoutPage`, add `useBeforeUnload` or `window.onbeforeunload` to warn user during payment processing (`currentStep === 3 || currentStep === 4`). Use React Router's `useBlocker` or a custom prompt when navigating away during payment processing to show confirm dialog ("Hay un pago en proceso. ¿Estás seguro de que querés salir?"). On confirmation, reset payment state and stop polling.
  - Satisfies: REQ-CP10 (browser back button scenario), REQ-CP04 (polling cleanup)

## 7. Polish

- [x] 19. **Loading states for all async operations** — AddressSelector: skeleton cards (3 gray rectangles) while `useUserAddresses` fetches. CardPaymentForm: wrapper spinner while Brick initializes + mutation in-flight overlay. PaymentResult: animated spinner with "Procesando tu pago..." message during polling. CheckoutPage: full-page skeleton on initial pedido fetch.
  - Satisfies: REQ-CP10, NFR-CP01

- [x] 20. **Empty states with user guidance** — AddressSelector: illustration + "No tenés direcciones guardadas" + "Agregar dirección" button → `/direcciones`. Cart empty (edge case in CheckoutPage): toast "Tu carrito está vacío. Agregá productos antes de pagar." → redirect `/productos`. No payment methods (Brick fails to load): error message + retry button.
  - Satisfies: REQ-CP10

- [x] 21. **Error states with user-friendly messages** — Map `status_detail` codes to Spanish messages (e.g., `cc_rejected_insufficient_amount` → "Fondos insuficientes. Probá con otra tarjeta.", `cc_rejected_card_disabled` → "Tarjeta rechazada. Contactá a tu banco o usá otra tarjeta."). Network errors: "Error de conexión. Verificá tu internet." 422 errors from backend: show backend message directly. Brick load failure: "No se pudo cargar el formulario de pago. Intentá de nuevo más tarde." + retry button.
  - Satisfies: REQ-CP06, REQ-CP10

- [x] 22. **Toast notifications for all key events** — Create pedido (info), pedido creation failure (error), payment approved (success), payment rejected (warning/error), network error (error), token expired (error), address fetch failure (error), payment in progress warning on retry attempt (warning). All via `useUIStore.addToast()`.
  - Satisfies: NFR-CP04

- [x] 23. **Mobile responsive layout** — CheckoutPage: progress indicator collapses to dots on mobile (`<768px`). AddressSelector cards: full width, min 44px tap targets. CheckoutSummary: condensed on mobile, expanded on desktop (≥768px) with side-by-side layout. CardPaymentForm: full width. PaymentResult: stacked vertically. Buttons: full width on mobile, auto width on desktop. Order summary: visible as sticky section on mobile.
  - Satisfies: NFR-CP03

- [x] 24. **WCAG AA accessibility compliance** — Add `role="alert"` and `aria-live="polite"` to toast container (verify existing implementation). Ensure Brick form is keyboard-navigable (handled by MP SDK). Add `aria-label` to progress indicator steps. Ensure color contrast meets WCAG AA minimum (4.5:1 for text). Add focus ring styles to all interactive elements.
  - Satisfies: NFR-CP05
