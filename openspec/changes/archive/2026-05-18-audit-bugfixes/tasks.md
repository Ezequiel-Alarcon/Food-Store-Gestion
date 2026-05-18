# Tasks: audit-bugfixes

> **Fuentes:** auditoría de código (39 bugs) + cotejo spec vs código (20 discrepancias)  
> **Estrategia:** fixes críticos/altos ahora, el resto documentado como deuda técnica

---

## ✅ YA APLICADOS — Backend (auditoría de código)

- [x] B1. `admin/service.py` — Agregar `total_usuarios` al response de `get_general_metrics()`
- [x] B2. `admin/router.py:231` — `h.actor_tipo.value` → `h.actor_tipo`
- [x] B3. `admin/router.py:34-36` — Session leak: `_get_service()` con `Depends(get_session)`
- [x] B4. `usuarios/schemas.py` — `from_attributes=True` en `UserRead` y `UserListResponse`
- [x] B5. `categorias/repository.py` — Bind params en CTEs (anti SQL injection)
- [x] B6. `pagos/service.py:282` — Usar `fsm.confirmar_pedido()` en vez de duplicar
- [x] B7. `productos/router.py:322` — Eliminar `return None` inalcanzable
- [x] B8. `productos/schemas.py:215` — `items: list` → `items: list[Any]`
- [x] B9. `db/seed.py` — Eliminar import `FormaPago` + `seed_formas_pago()` muertos
- [x] B10. `core/deps.py` — Mover `session.get(Usuario, sub)` fuera del try/except
- [x] B11. `ingredientes/service.py` — Renombrar `list()` → `list_all()`
- [x] B12. `productos/schemas.py` — `precio: float` → `precio: Decimal`

## ✅ YA APLICADOS — Frontend (auditoría de código)

- [x] F1. CREAR `lib/api.ts` — Axios + JWT interceptor + auto-refresh (estaba borrado)
- [x] F2. `PaymentResult.tsx` — `navigate(/pedidos/:id)` → `navigate('/pedidos')`
- [x] F3. `UsersPage.tsx:39` — `const [page, setPage]`, paginación funcional
- [x] F4. `OrderDetailPage.tsx` — `costo_envio` y `total` como props (ya no $0 hardcodeado)
- [x] F5. `paymentStore.ts` — `startCheckout(pedidoId)` recibe y guarda el parámetro
- [x] F6. `paymentStore.ts` — `get()` antes de `set()`, limpia timeout previo correctamente
- [x] F7. `DashboardPage.tsx` — Eliminado wrapper `ProtectedRoute` redundante (FSD)
- [x] F8. `LoginForm.tsx` — `location.state?.from` para redirect post-login
- [x] F9. `perfil/queries.ts` — `useAuthStore` movido del entity al caller (FSD)
- [x] F10. `OrderDetailPage.tsx` — `any` → `OrderAdminDetail`, `OrderItemDetail`, `OrderHistoryItem`
- [x] F11. `OrdersListPage` + `OrderDetailPage` — `ESTADO_COLORS` unificado desde `constants.ts`
- [x] F12. `cartStore.ts` — `addItem` actualiza `personalizacion` en items existentes
- [x] F13. `authStore.ts` — FIXME documentando `window.location.href` (requiere refactor mayor)
- [x] F14. `usuario-admin/types.ts` — `GESTOR` agregado a `ROLES`
- [x] F16. `index.css` — Keyframes + clase `animate-slide-in`
- [x] F17. `CartSummary.tsx` — Botón "Ver carrito" en footer del drawer
- [x] F18. `MisDireccionesPage.tsx` — try/catch + render de errores de mutación

---

## ✅ APLICADOS — FSM (spec vs código)

- [x] S1. `pedidos/fsm.py` — `_CANCEL_ROLES["EN_PREP"]` agregado `"PEDIDOS"`
- [x] S2. `pedidos/service.py` — Restaurar stock al cancelar desde `EN_PREP` (no solo CONFIRMADO)
- [x] S3. `pedidos/fsm.py` + `service.py` — `check_advance_permission()`, CLIENT bloqueado de avances

## ✅ APLICADOS — API guards de seguridad (spec vs código)

- [x] S4. `auth/router.py` — `POST /logout`: `Depends(get_current_user)`, status 204, sin body
- [x] S5. `pedidos/router.py` — `PATCH /{id}/estado`: `require_role("ADMIN", "PEDIDOS")`
- [x] S6. `admin/router.py` — `GET /metrics`: restringido a `require_role("ADMIN")`
- [x] S7. `productos/router.py` — `POST /`: `require_role("ADMIN")` (sin STOCK)
- [x] S8. `productos/router.py` — `PUT /{id}`: `require_role("ADMIN")` (sin STOCK)

---

> **Deuda técnica documentada:** Las 12 desviaciones spec vs código (D1-D12) fueron movidas al change [`intentional-bug-recommendations`](../../changes/intentional-bug-recommendations/tasks.md).
