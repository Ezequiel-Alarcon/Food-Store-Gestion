# Proposal: mvp-critical-fixes

## Why

La auditoría del 2026-05-18 reveló bugs críticos que impiden la grabación del video demo. El flujo de checkout está roto (carrito se vacía antes de llegar), el logout no revoca tokens, la FSM es inoperable desde el frontend, y la página de stock es un placeholder vacío. Estos 4 fixes desbloquean la funcionalidad MVP necesaria para mostrar el sistema funcionando end-to-end en el video.

## What Changes

- **Fix 1 — Checkout flow:** `CartPage` vacía el carrito DESPUÉS del pago exitoso (step 4: approved), no antes de navegar a checkout. `CheckoutPage` obtiene datos del pedido desde el backend usando `pedidoId` en vez de depender del carrito local.
- **Fix 2 — FSM transitions UI:** Agregar componente `StateTransition` en `OrderDetailPage` con botones para avanzar/cancelar estados según FSM y rol del usuario (ADMIN/PEDIDOS). Incluye motivo obligatorio al cancelar.
- **Fix 3 — Stock management:** Reemplazar el placeholder `<div>` de `/admin/stock` por una tabla real con productos, campos editables de stock, y toggle de activo/disable. Usa TanStack Query para fetching.
- **Fix 4 — Logout seguro:** `authStore.logout()` llama a `POST /api/v1/auth/logout` con el refresh token antes de limpiar estado local. Manejo silencioso de errores (token ya revocado, red caída).

## Capabilities

### New Capabilities

- `stock-management-ui`: Interfaz de gestión de stock para rol STOCK/ADMIN con tabla de productos, edición inline de cantidad y toggle de disponibilidad.

### Modified Capabilities

Ninguna. Los endpoints y specs existentes no cambian — solo se arregla el frontend para usarlos correctamente.

## Impact

- **Archivos:** ~6 frontend (`CartPage.tsx`, `CheckoutPage.tsx`, `OrderDetailPage.tsx`, `RouterProvider.tsx`, `authStore.ts`, + nuevo `StockManagementPage.tsx`)
- **Riesgo:** Medio — cambios en flujo de checkout (crítico para demo) y auth store (logout)
- **Dependencias:** Backend existente sin cambios. Endpoints ya implementados y funcionales.
