# Tasks: mvp-critical-fixes

> **Objetivo:** Arreglar 4 bugs críticos que bloquean la demo en video.  
> **Tiempo estimado:** 2-3 horas.  
> **Backend:** Sin cambios. Solo frontend.

---

## 1. Fix Checkout Flow (carrito → pago funcional)

- [x] 1.1 `CartPage.tsx` — No limpiar carrito antes de navegar a checkout. Mover `clearCart()` a después del pago exitoso (o eliminarlo, se limpiará en PaymentResult step 4).
- [x] 1.2 `CheckoutPage.tsx` — Obtener datos del pedido desde backend: `useQuery(['pedido', pedidoId], () => api.get(\`/pedidos/${pedidoId}\`))` en vez de depender de `cartStore.items`.
- [x] 1.3 `CheckoutPage.tsx` — Eliminar el redirect `if (items.length === 0)` que rompe el flujo. Reemplazar por loading spinner mientras carga el pedido.
- [x] 1.4 `PaymentResult.tsx` o `CartPage.tsx` — Limpiar carrito solo en step `approved` (pago exitoso confirmado).
- [x] 1.5 Probar flujo completo: catálogo → agregar al carrito → checkout → dirección → pago (simulado) → confirmación.
- [x] 4.4 Probar: login → logout → verificar que el refresh token queda revocado (usar endpoint admin de refreshtokens).
- [x] 5.1 Probar flujo completo de demo: registro → login → catálogo → carrito → checkout → pago → tracking de pedido.
- [x] 5.2 Probar panel admin: dashboard → lista de pedidos → transición de estado → gestión de stock.
- [x] 5.3 Probar logout + login (verificar que tokens se revocan).
- [x] 5.4 `openspec status --change "mvp-critical-fixes"` — confirmar artifacts completos.
