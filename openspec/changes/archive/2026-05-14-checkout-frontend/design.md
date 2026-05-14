# Design: checkout-frontend

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CHECKOUT FLOW                                   │
│                                                                              │
│  CartPage                     CheckoutPage (/checkout?pedido={id})           │
│  ┌──────────┐                 ┌────────────────────────────────────────────┐ │
│  │ Cart     │  "Finalizar"    │  STEP 1          STEP 2         STEP 3     │ │
│  │ Summary  │─────────────►   │  Address      →  Order       →  Card       │ │
│  │          │  POST pedidos   │  Selection       Summary        Payment     │ │
│  └──────────┘                 │                                            │ │
│                               │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │ │
│                               │  │Address   │  │Checkout  │  │CardPay-  │ │ │
│                               │  │Selector  │  │Summary   │  │mentForm  │ │ │
│                               │  │(entities │  │(Zustand  │  │(@mp/sdk- │ │ │
│                               │  │/address) │  │cart)     │  │react)    │ │ │
│                               │  └────┬─────┘  └────┬─────┘  └────┬─────┘ │ │
│                               │       │              │              │       │ │
│                               │       ▼              │         ┌────▼─────┐ │ │
│                               │  TanStack Query      │         │onSubmit  │ │ │
│                               │  useUserAddresses()  │         │{token,   │ │ │
│                               │                      │         │pm_id}    │ │ │
│                               └──────────────────────┼─────────┼──────────┘ │
│                                                      │         │            │
│                                                      │    POST /api/v1/     │
│                                                      │    pagos/crear       │
│                                                      │    {pedido_id,       │
│                                                      │     payment_method,  │
│                                                      │     token}           │
│                                                      │         │            │
│                                                      │         ▼            │
│                                                      │    ┌──────────┐      │
│                                                      │    │ Payment  │      │
│                                                      │    │ Result   │      │
│                                                      │    │ (Step 4) │      │
│                                                      │    └────┬─────┘      │
│                                                      │         │            │
│                                                      │    Poll GET /api/v1/ │
│                                                      │    pagos/{pedido_id} │
│                                                      │         │            │
│                                                      │    ┌────▼─────┐      │
│                                                      │    │Redirect  │      │
│                                                      │    │/pedidos/ │      │
│                                                      │    │{id}      │      │
│                                                      │    └──────────┘      │
└──────────────────────────────────────────────────────────────────────────────┘

                         ┌─────────────────────────────┐
                         │       DATA LAYERS           │
                         ├──────────┬──────────────────┤
                         │ Zustand  │ TanStack Query   │
                         ├──────────┼──────────────────┤
                         │ cartStore│ addresses (list) │
                         │ payment  │ pagos (create,   │
                         │ Store    │   poll status)   │
                         │ uiStore  │ pedidos (detail) │
                         │ (toasts) │                  │
                         └──────────┴──────────────────┘
```

### Flow step-by-step

1. User clicks "Finalizar pedido" in Cart → `POST /api/v1/pedidos` (creates pedido with `direccion_id` + items)
2. Redirect to `/checkout?pedido={id}`
3. **Step 1 — Address**: Select/confirm delivery address via `useUserAddresses()` (TanStack Query)
4. **Step 2 — Summary**: Review cart items from `useCartStore`, totals, selected address
5. **Step 3 — Payment**: CardPayment Brick renders → user fills card → `onSubmit` fires with `{token, payment_method_id, ...}`
6. Client calls `POST /api/v1/pagos/crear` with `{pedido_id, payment_method_id, token}`
7. **Step 4 — Result**: Poll `GET /api/v1/pagos/{pedido_id}` every 3s until terminal status, or show StatusScreen Brick, or custom result component
8. On `approved` → redirect to `/pedidos/{id}`; on `rejected` → offer retry

---

## 2. Backend Changes

### 2.1 Schema: `PagoCreate` — add `token` field

**File:** `backend/app/modules/pagos/schemas.py`

```python
class PagoCreate(BaseModel):
    """Schema para crear un pago."""
    pedido_id: int
    payment_method_id: str = "account_money"
    token: Optional[str] = None  # ← NEW: card token from MP SDK frontend
```

### 2.2 Service: pass `token` to MercadoPago API

**File:** `backend/app/modules/pagos/service.py` — `crear_pago` method (line ~189)

Inside `crear_pago`, after building `payment_data`, add:

```python
# If a card token is provided (Checkout Transparente), include it
if data.token:
    payment_data["token"] = data.token
```

This must go BEFORE the `sdk.payment().create(payment_data, request_options)` call (line 202). The `token` field tells MP to process this as a card payment using the previously tokenized card.

**No change needed in `reintentar_pago`** — retries currently don't accept a new token.

### 2.3 Endpoints — no changes

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/pagos/crear` | POST | Create payment (now accepts `token`) |
| `/api/v1/pagos/{pedido_id}` | GET | Poll payment status |
| `/api/v1/pagos/{pedido_id}/reintentar` | POST | Retry rejected payment |

The existing `PagoCreate` schema is validated by FastAPI automatically — adding the `token` field makes it available in `data.token`.

### 2.4 Rationale

- `token` is `Optional[str]` because non-card payments (Rapipago, Pago Fácil, account_money) don't need it
- Token is sent from frontend CardPayment Brick — never raw card data touches our server (PCI SAQ-A compliant)
- The token is a one-time-use string generated by MercadoPago's JS SDK in the browser

---

## 3. Frontend Architecture

### 3.1 New entity: `entities/pago/`

Following the existing pattern from `entities/addresses/` and `entities/pedido/`:

```
entities/pago/
├── types.ts      # PagoResponse, PagoCreate, PagoStatus
├── api.ts        # pagosApi: create, getByPedidoId, retry
├── queries.ts    # useCreatePago, usePagoStatus (polling), useRetryPago
└── index.ts      # barrel exports
```

#### `entities/pago/types.ts`

```typescript
export interface PagoCreate {
  pedido_id: number
  payment_method_id: string
  token?: string | null
}

export interface PagoResponse {
  id: number
  pedido_id: number
  mp_payment_id: number | null
  idempotency_key: string
  external_reference: string
  status: PagoStatus
  status_detail: string | null
  payment_method_id: string | null
  transaction_amount: number
  creado_en: string
  actualizado_en: string
}

export type PagoStatus =
  | 'pending'
  | 'approved'
  | 'rejected'
  | 'in_process'
  | 'cancelled'
  | 'refunded'
```

#### `entities/pago/api.ts`

```typescript
import { api } from '../../lib/api'
import type { PagoCreate, PagoResponse } from './types'

export const pagosApi = {
  create: async (payload: PagoCreate): Promise<PagoResponse> => {
    const res = await api.post<PagoResponse>('/pagos/crear', payload)
    return res.data
  },

  getByPedidoId: async (pedidoId: number): Promise<PagoResponse> => {
    const res = await api.get<PagoResponse>(`/pagos/${pedidoId}`)
    return res.data
  },

  retry: async (pedidoId: number): Promise<PagoResponse> => {
    const res = await api.post<PagoResponse>(`/pagos/${pedidoId}/reintentar`)
    return res.data
  },
}
```

#### `entities/pago/queries.ts`

```typescript
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { pagosApi } from './api'
import type { PagoCreate, PagoStatus } from './types'

const keys = {
  pagoByPedido: (pedidoId: number) => ['pago', pedidoId] as const,
}

export function useCreatePago() {
  return useMutation({
    mutationFn: (payload: PagoCreate) => pagosApi.create(payload),
  })
}

export function usePagoStatus(
  pedidoId: number | null,
  enabled: boolean
) {
  return useQuery({
    queryKey: keys.pagoByPedido(pedidoId!),
    queryFn: () => pagosApi.getByPedidoId(pedidoId!),
    enabled: enabled && pedidoId !== null,
    refetchInterval: (query) => {
      const status: PagoStatus = query.state.data?.status
      // Poll every 3s while pending/in_process, stop on terminal states
      if (status === 'pending' || status === 'in_process') return 3000
      return false
    },
  })
}

export function useRetryPago() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (pedidoId: number) => pagosApi.retry(pedidoId),
    onSuccess: (_, pedidoId) => {
      qc.invalidateQueries({ queryKey: keys.pagoByPedido(pedidoId) })
    },
  })
}
```

### 3.2 New page: `pages/CheckoutPage.tsx`

Route-level component. Orchestrates the multi-step wizard. Does NOT contain heavy logic — delegates to feature components.

```typescript
// pages/CheckoutPage.tsx
export function CheckoutPage() {
  const pedidoId = /* extract from searchParams */
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1)
  const [selectedAddressId, setSelectedAddressId] = useState<number | null>(null)
  // ...
}
```

**States managed locally (useState):**
- `currentStep` (1–4): which wizard step is active
- `selectedAddressId`: user's chosen delivery address

### 3.3 Feature components: `features/checkout/`

```
features/checkout/
├── AddressSelector.tsx     # Step 1 — list addresses, select one
├── CheckoutSummary.tsx     # Step 2 — cart items + totals + selected address
├── CardPaymentForm.tsx     # Step 3 — CardPayment Brick integration
├── PaymentResult.tsx       # Step 4 — StatusScreen Brick or custom result
└── index.ts                # barrel exports
```

#### `AddressSelector.tsx`
- Uses `useUserAddresses()` from `entities/addresses/`
- Renders radio/list of saved addresses
- Emits `onSelect(addressId: number)` callback
- Shows loading skeleton while query is fetching
- Empty state: link to `/direcciones` to add one

#### `CheckoutSummary.tsx`
- Reads `items` from `useCartStore`
- Computes subtotal, total via `totalPrice()` selector
- Displays selected address summary (derived from address query cache)
- "Confirmar y pagar" button → advances to step 3

#### `CardPaymentForm.tsx` — THE CRITICAL COMPONENT

```tsx
import { CardPayment } from '@mercadopago/sdk-react'
import type { CardPaymentBrickData } from '@mercadopago/sdk-react'

interface CardPaymentFormProps {
  pedidoId: number
  amount: number  // total in ARS (float, e.g. 1500.00)
  onSuccess: (pagoResponse: PagoResponse) => void
  onError: (error: Error) => void
}

export function CardPaymentForm({ pedidoId, amount, onSuccess, onError }: CardPaymentFormProps) {
  const createPago = useCreatePago()
  const addToast = useUIStore((s) => s.addToast)

  const handleSubmit = async (formData: CardPaymentBrickData) => {
    try {
      const result = await createPago.mutateAsync({
        pedido_id: pedidoId,
        payment_method_id: formData.payment_method_id,
        token: formData.token,
      })
      onSuccess(result)
    } catch (err) {
      addToast('error', 'Error al procesar el pago')
      onError(err as Error)
    }
  }

  return (
    <CardPayment
      initialization={{ amount }}
      onSubmit={handleSubmit}
      onError={(error) => {
        addToast('error', 'Error en el formulario de pago')
        onError(new Error(error))
      }}
    />
  )
}
```

**Brick lifecycle management:**
- CardPayment Brick auto-mounts when component mounts
- Auto-unmounts on component unmount (handled by SDK internally)
- **IMPORTANT**: If user navigates back and re-enters step 3, the component remounts → Brick re-renders fresh. This is correct behavior — no manual `controller.unmount()` needed because React unmounts the DOM node.

#### `PaymentResult.tsx`
- Receives `pagoResponse` from card payment
- Option A: Uses `StatusScreen` Brick to show MP-branded result
- Option B: Custom result UI with success/rejected/pending states
- Polls `GET /api/v1/pagos/{pedido_id}` for async methods
- On `approved` → auto-redirect to `/pedidos/{id}` after 3s
- On `rejected` → show "Reintentar" button calling `POST /api/v1/pagos/{id}/reintentar`
- On `pending` / `in_process` → show spinner with polling message

### 3.4 Route registration

**File:** `frontend/src/providers/RouterProvider.tsx`

Add inside `<Routes>`:

```tsx
<Route
  path="/checkout"
  element={
    <ProtectedRoute allowedRoles={['CLIENT']}>
      <CheckoutPage />
    </ProtectedRoute>
  }
/>
```

Import:
```tsx
import { CheckoutPage } from '../pages/CheckoutPage'
```

### 3.5 MercadoPago SDK initialization

**File:** `frontend/src/main.tsx`

Add BEFORE `createRoot(...).render(...)`:

```tsx
import { initMercadoPago } from '@mercadopago/sdk-react'

initMercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY, {
  locale: 'es-AR',
})
```

The SDK init must be called exactly ONCE, before any Brick renders. `main.tsx` is the correct place — it's the app entry point, loaded before any route.

**Environment variable:**
```
VITE_MP_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

This key is the PUBLIC key (starts with `TEST-` for sandbox, `APP_USR-` for production). It's safe to expose in the frontend — MP requires it for client-side tokenization.

### 3.6 Zustand store: `usePaymentStore` — notes

The existing `usePaymentStore` was designed for Checkout Pro (redirect-based flow). For Checkout Transparente, it is **partially reused**:

| Field | Checkout Pro usage | Checkout Transparente usage |
|-------|-------------------|---------------------------|
| `checkoutStep` | `redirecting` state | Maps to `processing`, `approved`, `rejected`, `error` |
| `preferenceId` | Stores MP preference | **NOT USED** — leave as null |
| `paymentStatus` | Webhook result | Polling result |
| `statusDetail` | Webhook detail | Polling detail |
| `startCheckout()` | Sets `creating` | Can be reused |
| `updatePaymentStatus()` | From webhook | From polling result |
| `resetPayment()` | After redirect | On checkout unmount |

The `startCheckout()` setter currently takes a `pedidoId` parameter but doesn't use it. This is fine — the parameter is ignored. We call `resetPayment()` when the user leaves the checkout page (useEffect cleanup in `CheckoutPage`).

---

## 4. Data Flow

### 4.1 State management boundary

```
┌──────────────────────────────────────────────────┐
│                 CHECKOUT STATE                    │
├─────────────────┬────────────────────────────────┤
│ ZUSTAND         │ TANSTACK QUERY                 │
│ (client state)  │ (server state)                 │
├─────────────────┼────────────────────────────────┤
│ cartStore:      │ useUserAddresses()             │
│   items[]       │   → list of saved addresses    │
│   total         │                                │
│                 │ useCreatePago() (mutation)      │
│ paymentStore:   │   → POST /pagos/crear          │
│   checkoutStep  │                                │
│   paymentStatus │ usePagoStatus(pedidoId) (query) │
│                 │   → GET /pagos/{pedidoId}       │
│ uiStore:        │   → polling every 3s           │
│   addToast()    │                                │
│                 │ useRetryPago() (mutation)       │
│                 │   → POST /pagos/{id}/reintentar │
├─────────────────┴────────────────────────────────┤
│ LOCAL STATE (useState in CheckoutPage)            │
│   currentStep: 1 | 2 | 3 | 4                     │
│   selectedAddressId: number | null                │
└──────────────────────────────────────────────────┘
```

**Rule enforced:** No server data in Zustand. No cart data in TanStack Query.

### 4.2 Polling strategy

```
Payment created
      │
      ▼
┌──────────┐   poll GET /pagos/{pedido_id} every 3s
│ pending  │────────────────────────────────┐
│in_process│                                │
└────┬─────┘                                │
     │ terminal?                             │
     ├── YES: stop polling                   │
     │   ├── approved → redirect /pedidos/   │
     │   ├── rejected → show retry button    │
     │   └── cancelled/refunded → show msg   │
     └── NO: continue polling                │
```

Implementation via TanStack Query `refetchInterval` (see `usePagoStatus` in section 3.1):

```typescript
refetchInterval: (query) => {
  const status = query.state.data?.status
  if (status === 'pending' || status === 'in_process') return 3000
  return false  // stop polling on terminal states
}
```

**Why TanStack Query for polling and not useEffect + setInterval?**
- Automatic cleanup on unmount
- Deduplication: multiple components won't trigger duplicate polls
- `staleTime: 0` ensures fresh data every poll
- Cached data available for navigation back

**Max poll duration:** 5 minutes. After that, show "El pago está demorando más de lo esperado. Te notificaremos cuando se confirme." The webhook will update the order status server-side regardless.

### 4.3 Error handling matrix

| Step | Error | Handling |
|------|-------|----------|
| Page load | No `pedido` query param | Toast "Pedido no encontrado" → redirect `/carrito` |
| Page load | Pedido doesn't belong to user | Toast "No tenés acceso" → redirect `/pedidos` |
| Step 1 | No addresses in account | Show empty state with CTA "Agregar dirección" → `/direcciones` |
| Step 2 | Cart empty (edge case) | Toast "Carrito vacío" → redirect `/carrito` |
| Step 3 | CardPayment Brick load failure | Toast + retry button |
| Step 3 | `POST /pagos/crear` 4xx | Show error message from API |
| Step 3 | `POST /pagos/crear` 5xx / network | Toast "Error de conexión. Reintentá." |
| Step 3 | Card rejected by MP (`formData` has error) | Brick shows inline errors (handled by SDK) |
| Step 4 | Polling 404 (pago not yet created) | Retry, show "Procesando..." |
| Step 4 | Polling 5xx / network | Continue polling (transient), toast after 3 failures |
| Step 4 | Token expired (MP rejects `token`) | Toast "La sesión de pago expiró. Volvé a intentarlo." → back to step 3 |
| Any step | Browser refresh | Component remounts, reads `pedido` from URL, restores step 1 |

### 4.4 Sequence diagram: payment submission + polling

```
User                CardPaymentForm        API              MP SDK          PagoStatus Query
 │                       │                  │                  │                  │
 │  fill card form       │                  │                  │                  │
 │──────────────────────►│                  │                  │                  │
 │                       │                  │                  │                  │
 │                       │  tokenize()      │                  │                  │
 │                       │─────────────────────────────────────►│                  │
 │                       │  {token, pm_id}  │                  │                  │
 │                       │◄─────────────────────────────────────│                  │
 │                       │                  │                  │                  │
 │                       │  POST /pagos/crear                  │                  │
 │                       │  {pedido_id, token, pm_id}          │                  │
 │                       │─────────────────►│                  │                  │
 │                       │                  │  payment.create  │                  │
 │                       │                  │─────────────────►│                  │
 │                       │                  │  PagoResponse    │                  │
 │                       │  PagoResponse    │◄─────────────────│                  │
 │                       │◄─────────────────│                  │                  │
 │                       │                  │                  │                  │
 │  onSuccess(response)  │                  │                  │                  │
 │◄──────────────────────│                  │                  │                  │
 │                       │                  │                  │                  │
 │  render PaymentResult │                  │                  │                  │
 │──────────────────────►│                  │                  │                  │
 │                       │                  │                  │                  │
 │                       │                  │  start polling   │                  │
 │                       │                  │──────────────────────────────────►│
 │                       │                  │                  │  GET /pagos/{id} │
 │                       │                  │◄──────────────────────────────────│
 │                       │                  │  {status: "pending"}               │
 │                       │                  │──────────────────────────────────►│
 │                       │                  │                  │  ...wait 3s...   │
 │                       │                  │                  │  GET /pagos/{id} │
 │                       │                  │  {status: "approved"}              │
 │                       │                  │◄──────────────────────────────────│
 │                       │                  │  stop polling     │                  │
 │                       │                  │                  │                  │
 │  redirect /pedidos/id │                  │                  │                  │
 │◄──────────────────────│                  │                  │                  │
```

---

## 5. UI/UX Decisions

### 5.1 Multi-step wizard — NOT single page

**Decision:** 4-step wizard with progress indicator.

**Rationale:**
- Reduces cognitive load (one decision at a time)
- Prevents user from submitting card before seeing order summary
- Each step has independent loading/error states
- Matches e-commerce UX patterns (MercadoLibre, Amazon)

**Progress indicator:**

```
[1. Dirección] ─── [2. Resumen] ─── [3. Pago] ─── [4. Resultado]
     ●                  ○               ○              ○
```

- Current step: filled circle `●`, bold text
- Completed steps: filled circle `●`, normal text, clickable (go back)
- Future steps: empty circle `○`, muted text, disabled

### 5.2 Loading states

| Component | Loading state |
|-----------|--------------|
| AddressSelector | Skeleton cards (3 gray rectangles) while `useUserAddresses` fetches |
| CheckoutSummary | Cart items render instantly (Zustand is sync). No loading needed. |
| CardPaymentForm | Brick has built-in skeleton (handled by MP SDK). Plus a wrapper spinner while mutation is in-flight. |
| PaymentResult | Animated spinner with "Procesando tu pago..." message. Pulsing dots. |

### 5.3 Toast notifications

Using existing `useUIStore.addToast()`:

| Trigger | Type | Message |
|---------|------|---------|
| Pedido creation failure | `error` | "No se pudo crear el pedido. Revisá tu carrito." |
| Address fetch failure | `error` | "No se pudieron cargar tus direcciones." |
| Payment rejected | `warning` | "El pago fue rechazado. Probá con otra tarjeta." |
| Payment approved | `success` | "¡Pago aprobado! Redirigiendo a tu pedido..." |
| Network error | `error` | "Error de conexión. Verificá tu internet." |
| Token expired | `error` | "La sesión de pago expiró. Volvé a intentarlo." |

### 5.4 Mobile responsiveness

- Wizard steps stack vertically on mobile (`flex-col`)
- CardPayment Brick is responsive by default (MP SDK handles this)
- Address cards: full width, large tap targets (min 44px height)
- Order summary: condensed on mobile, expanded on desktop (≥768px)
- Buttons: full width on mobile, auto width on desktop
- Progress indicator: horizontal dots on mobile, horizontal bar with labels on desktop

### 5.5 Navigation guards

- **Browser back button in step 3:** User goes back to step 2. CardPayment Brick unmounts cleanly. No card data is retained (PCI compliant).
- **Browser back button in step 4 during polling:** Polling stops (TanStack Query `enabled: false` on unmount). If user navigates forward again, polling resumes from cache.
- **Direct URL access (`/checkout` without pedido):** Redirect to `/carrito` with toast.
- **Refreshing during checkout:** Step resets to 1. Address and cart data reload from TanStack Query cache / network.

### 5.6 Empty states

- **No addresses:** Illustration + "No tenés direcciones guardadas" + "Agregar dirección" button → `/direcciones`
- **Cart empty (edge case):** "Tu carrito está vacío" + "Volver a la tienda" button → `/productos`
- **No payment methods (MP SDK fails to load):** "No se pudo cargar el formulario de pago. Reintentá."

---

## 6. Testing Strategy

### 6.1 What to test

| Target | Tests | Tool |
|--------|-------|------|
| `entities/pago/api.ts` | API functions return correct shapes | Vitest + MSW or mock `api` |
| `entities/pago/queries.ts` | Polling stops on terminal status, mutation invalidates cache | Vitest + `@tanstack/react-query` testing utils |
| `AddressSelector` | Renders addresses, handles empty state, calls `onSelect` | Vitest + React Testing Library |
| `CheckoutSummary` | Computes totals correctly, displays cart items | Vitest + RTL |
| `CardPaymentForm` | Calls `useCreatePago` on submit, handles loading/error | Vitest + RTL + mock SDK |
| `PaymentResult` | Shows correct UI per status, polls, redirects on approved | Vitest + RTL |
| `CheckoutPage` | Wizard navigation, step transitions, error boundaries | Vitest + RTL + React Router memory router |
| Backend `PagoCreate` | Validates `token` optional field, accepts with/without | Pytest |
| Backend `crear_pago` | Includes `token` in MP request when provided | Pytest + mock MP SDK |

### 6.2 Mocking the MP SDK

The CardPayment Brick renders an iframe (MP-hosted). We can't test the actual card form in unit tests. Strategy:

```typescript
// __mocks__/@mercadopago/sdk-react.ts
vi.mock('@mercadopago/sdk-react', () => ({
  initMercadoPago: vi.fn(),
  CardPayment: vi.fn(({ onSubmit, onError }: any) => {
    // Return a mock component that exposes buttons to trigger callbacks
    const MockCardPayment = () => (
      <div data-testid="card-payment-mock">
        <button
          data-testid="submit-payment"
          onClick={() => onSubmit({
            token: 'mock-token-abc123',
            payment_method_id: 'visa',
            issuer_id: '200',
            installments: 1,
          })}
        >
          Pay
        </button>
        <button
          data-testid="error-payment"
          onClick={() => onError?.('card_declined')}
        >
          Error
        </button>
      </div>
    )
    return <MockCardPayment />
  }),
  StatusScreen: vi.fn(({ initialization }: any) => (
    <div data-testid="status-screen-mock">
      Payment ID: {initialization.paymentId}
    </div>
  )),
}))
```

This allows testing:
1. The `onSubmit` callback fires with correct data
2. The component calls `useCreatePago.mutateAsync`
3. Error handling paths
4. Component renders in different states

### 6.3 TanStack Query testing

```typescript
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

function createWrapper() {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  )
}

test('usePagoStatus stops polling on approved', async () => {
  // Mock api.get to return { status: 'approved' }
  const { result } = renderHook(
    () => usePagoStatus(1, true),
    { wrapper: createWrapper() }
  )
  await waitFor(() => {
    expect(result.current.data?.status).toBe('approved')
  })
  // Verify refetchInterval returned false
})
```

### 6.4 Backend tests

```python
# tests/test_pagos.py
def test_crear_pago_con_token_card():
    """Token de tarjeta se incluye en el request a MP."""
    data = PagoCreate(pedido_id=1, payment_method_id="visa", token="tok_abc123")
    with patch("mercadopago.SDK") as mock_sdk:
        mock_sdk.return_value.payment.return_value.create.return_value = {...}
        service.crear_pago(data, mock_user)
        call_args = mock_sdk.return_value.payment.return_value.create.call_args[0][0]
        assert call_args["token"] == "tok_abc123"

def test_crear_pago_sin_token_rapipago():
    """Pago en efectivo no incluye token."""
    data = PagoCreate(pedido_id=1, payment_method_id="rapipago")
    with patch("mercadopago.SDK") as ...:
        ...
        assert "token" not in call_args
```

---

## 7. Risks & Mitigations

### Risk 1: `@mercadopago/sdk-react` v0.0.12 instability

**Probability:** Medium
**Impact:** High — Brick may fail to render, break on updates, or have missing APIs

**Mitigations:**
- Pin exact version `0.0.12` in `package.json` (already done)
- Wrap Brick in an `<ErrorBoundary>` to catch render failures
- Add fallback UI: "El formulario de pago no está disponible. Intentá de nuevo en unos minutos."
- Test across Chrome, Firefox, Safari, and mobile browsers
- Monitor MP SDK changelog for breaking changes before upgrading

### Risk 2: Card token expiration

**Probability:** Low
**Impact:** Medium — user fills card form but token expires before backend uses it

**Mitigations:**
- MP tokens typically last 5–10 minutes (documented by MP)
- POST to `/api/v1/pagos/crear` happens immediately after tokenization (same JS event loop tick)
- If backend returns 4xx for expired token, show toast and reset to step 3 (Brick remounts with fresh token)
- **Do NOT store the token** in any state — use it immediately and discard

### Risk 3: Browser back button during checkout

**Probability:** High
**Impact:** Medium — user could leave payment in `pending` or `in_process` state

**Mitigations:**
- `usePaymentStore.resetPayment()` in `CheckoutPage` useEffect cleanup
- CardPayment Brick unmounts on navigation, no card data retained
- Polling stops automatically on unmount (TanStack Query `enabled` guard)
- If user returns to `/checkout?pedido={id}`, page checks if a payment already exists (via `usePagoStatus`) and shows step 4 instead of starting over
- The webhook will eventually process the payment server-side regardless of client state

### Risk 4: Network failure during payment submission

**Probability:** Medium
**Impact:** High — user thinks payment failed but it may have succeeded

**Mitigations:**
- Idempotency key prevents double charges (backend already implements UUID-based keys)
- On network error, DO NOT auto-retry — show explicit message: "No pudimos confirmar si el pago se procesó. Verificá el estado en Mis Pedidos."
- Provide "Verificar estado" button that polls `GET /api/v1/pagos/{pedido_id}`
- Idempotency keys survive browser refresh (we generate a new one each submit attempt — which is correct per MP docs: new key = new attempt allowed)

### Risk 5: MP SDK conflicts with React StrictMode

**Probability:** Medium
**Impact:** Low — double-render in dev may cause Brick to mount twice

**Mitigations:**
- React StrictMode double-mounts components in development. The MP Brick should handle this since it creates iframes with unique IDs.
- If issues arise, guard with a `useRef` to prevent double initialization:
  ```typescript
  const initialized = useRef(false)
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true
      // ... init
    }
  }, [])
  ```
- Test thoroughly with StrictMode enabled in dev

### Risk 6: `usePaymentStore` schema mismatch

**Probability:** Low
**Impact:** Low — The store was designed for Checkout Pro (redirect flow). Fields like `preferenceId` are unused in Checkout Transparente.

**Mitigations:**
- We only use `checkoutStep`, `paymentStatus`, `statusDetail`, `updatePaymentStatus()`, `resetPayment()`
- `preferenceId` stays `null` — no code reads it except the unused `setPreference()`
- If confusion arises, document the dual-use in the store file with JSDoc comments
- Do NOT refactor the store in this change (scope creep) — it works for both flows

---

## 8. Files Changed Summary

### Backend (2 files)
| File | Change |
|------|--------|
| `backend/app/modules/pagos/schemas.py` | Add `token: Optional[str] = None` to `PagoCreate` |
| `backend/app/modules/pagos/service.py` | Conditionally include `token` in `payment_data` dict |

### Frontend (new files)
| File | Purpose |
|------|---------|
| `entities/pago/types.ts` | PagoCreate, PagoResponse, PagoStatus types |
| `entities/pago/api.ts` | Axios calls to `/pagos/*` endpoints |
| `entities/pago/queries.ts` | useCreatePago, usePagoStatus, useRetryPago |
| `entities/pago/index.ts` | Barrel exports |
| `features/checkout/AddressSelector.tsx` | Step 1: address selection component |
| `features/checkout/CheckoutSummary.tsx` | Step 2: order review component |
| `features/checkout/CardPaymentForm.tsx` | Step 3: CardPayment Brick integration |
| `features/checkout/PaymentResult.tsx` | Step 4: result display + polling |
| `features/checkout/index.ts` | Barrel exports |
| `pages/CheckoutPage.tsx` | Multi-step wizard orchestrator |

### Frontend (modified files)
| File | Change |
|------|--------|
| `main.tsx` | Add `initMercadoPago(VITE_MP_PUBLIC_KEY)` before render |
| `providers/RouterProvider.tsx` | Add `/checkout` route under `ProtectedRoute(['CLIENT'])` |

### Environment
| File | Change |
|------|--------|
| `.env.example` | Add `VITE_MP_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
