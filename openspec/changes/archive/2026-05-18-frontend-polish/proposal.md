# Proposal: frontend-polish

## Why

La demo en video necesita una UX pulida. OrdersPage usa `useState`/`useEffect` manual (sin TanStack Query), la búsqueda del catálogo es solo local (no usa backend search), y PaymentResult muestra estados de pago confusos (pending/in_process/cancelled todos igual). Estos fixes mejoran la calidad visual sin tocar backend.

## What Changes

- **OrdersPage → TanStack Query:** Reemplazar `useState`+`useEffect`+`fetchOrders` por `useQuery` con `refetchInterval: 30000` para polling automático cada 30s.
- **CatalogPage → search server-side:** Enviar `search` como query param al backend en vez de filtrar localmente con `Array.filter()`.
- **PaymentResult → estados claros:** Diferenciar visualmente `pending` (esperando), `in_process` (en revisión), `cancelled` (cancelado), `rejected` (rechazado).

## Capabilities

### Modified Capabilities

Ninguna. Cambios internos de frontend, no modifican specs.

## Impact

- **Archivos:** `OrdersPage.tsx`, `CatalogPage.tsx`, `PaymentResult.tsx`
- **Riesgo:** Bajo — refactors de componentes existentes
- **Dependencias:** Backend endpoints ya funcionales
