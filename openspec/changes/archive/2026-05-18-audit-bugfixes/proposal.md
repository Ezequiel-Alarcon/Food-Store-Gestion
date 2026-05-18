# Proposal: audit-bugfixes

## Why
Auditoría completa del código backend y frontend reveló **39 bugs de código** + **20 discrepancias spec vs código**. 
Se aplicaron 29 fixes de código (B1-B12, F1-F18). Quedan 8 fixes de spec-vs-código (FSM + API guards).
Las 12 desviaciones restantes se documentan como deuda técnica para futuros changes.

## What Changes

### Backend (17 bugs)
| # | Severidad | Archivo | Bug |
|---|-----------|---------|-----|
| B1 | 🔴 CRÍTICO | `admin/service.py:39` | `total_usuarios` faltante → 500 en `/admin/metrics/` |
| B2 | 🔴 CRÍTICO | `admin/router.py:231` | `.value` sobre `str` → AttributeError en historial |
| B3 | 🔴 CRÍTICO | `admin/router.py:34` | Session leak: `SessionLocal()` nunca cerrada |
| B4 | 🟠 ALTO | `usuarios/schemas.py:13,82` | Falta `from_attributes=True` en `UserRead` y `UserListResponse` |
| B5 | 🟠 ALTO | `categorias/repository.py:70-179` | SQL injection risk: f-strings en CTEs |
| B6 | 🟠 ALTO | `pagos/service.py:282` | No usa `fsm.confirmar_pedido()`, duplica validación |
| B7 | 🟡 MEDIO | `productos/router.py:322` | Código muerto: `return None` inalcanzable |
| B8 | 🟡 MEDIO | `productos/schemas.py:215` | `items: list` sin tipo genérico |
| B9 | 🟡 MEDIO | `db/seed.py:22` | Import `FormaPago` inexistente + función muerta |
| B10 | 🟡 MEDIO | `core/deps.py:81-92` | `ImportError` masking silencia validación de usuario |
| B11 | 🟡 MEDIO | `ingredientes/service.py:81` | Método `list()` sombrea built-in |
| B12 | 🟡 MEDIO | `productos/schemas.py:28,86` | `float` para `precio` (inexacto para dinero) |
| B13 | ⚪ BAJO | `ingredientes/model.py:46` | `actualizado_en` default `None` inconsistente |
| B14 | ⚪ BAJO | `tests/.../test_admin_metrics.py:113` | Test espera 200 pero endpoint crashea |
| B15 | ⚪ BAJO | `usuarios/schemas.py:23,92` | Tipo inconsistente `datetime` vs `str` |
| B16 | ⚪ BAJO | `productos/service.py:100-111` | Validación redundante de precio/stock |
| B17 | ⚪ BAJO | `refreshtokens/router.py:33-35` | `_get_service()` crea instancia nueva innecesaria |

### Frontend (22 bugs)
| # | Severidad | Archivo | Bug |
|---|-----------|---------|-----|
| F1 | 🔴 CRÍTICO | `lib/api.ts` | **NO EXISTE.** 10 archivos lo importan. App no compila. |
| F2 | 🔴 CRÍTICO | `features/checkout/PaymentResult.tsx:69,106,137` | Navega a `/pedidos/:id` (ruta inexistente para cliente) |
| F3 | 🟠 ALTO | `features/admin/users/ui/UsersPage.tsx:39` | `useState(1)` sin setter → paginación rota |
| F4 | 🟠 ALTO | `features/admin/orders/ui/OrderDetailPage.tsx:128,132` | `formatCurrency(0)` hardcodeados |
| F5 | 🟠 ALTO | `stores/paymentStore.ts:34` | `startCheckout` ignora parámetro `pedidoId` |
| F6 | 🟠 ALTO | `stores/paymentStore.ts:41-53` | Timeout cleanup dead code |
| F7 | 🟠 ALTO | `features/admin/dashboard/DashboardPage.tsx:5` | FSD violation: feature importa de sibling feature |
| F8 | 🟡 MEDIO | `features/auth/LoginForm.tsx:41` | Ignora `location.state.from` del redirect |
| F9 | 🟡 MEDIO | `entities/perfil/queries.ts:4` | FSD violation: entity importa de store |
| F10 | 🟡 MEDIO | `features/admin/orders/ui/OrderDetailPage.tsx` | Usa `any` en lugar de tipos definidos |
| F11 | 🟡 MEDIO | `features/admin/orders/ui/OrdersListPage.tsx:8-15` | `ESTADO_COLORS` duplicado sin `border-*` |
| F12 | 🟡 MEDIO | `stores/cartStore.ts:30-53` | `addItem` no actualiza `personalizacion` en items existentes |
| F13 | 🟡 MEDIO | `stores/authStore.ts:88` | `logout` usa `window.location.href` (full reload) |
| F14 | 🟡 MEDIO | `entities/usuario-admin/types.ts:22` | `ROLES` no incluye `GESTOR` |
| F15 | 🟡 MEDIO | `features/admin/dashboard/api/metricsApi.ts:36-65` | No envía `dateRange` a la API |
| F16 | 🟡 MEDIO | `features/layout/ToastContainer.tsx:21` | Clase CSS `animate-slide-in` no definida |
| F17 | 🟡 MEDIO | `features/cart/CartSummary.tsx:117-136` | Drawer sin link a checkout |
| F18 | 🟡 MEDIO | `features/addresses/MisDireccionesPage.tsx:42-51` | Sin error handling en submit |
| F19 | ⚪ BAJO | `features/auth/ProtectedRoute.tsx:6` | `allowedRoles` sin tipo union estricto |
| F20 | ⚪ BAJO | `features/layout/Navigation.tsx:47` | Solo usa primer rol para menú |
| F21 | ⚪ BAJO | `features/auth/ProtectedRoute.tsx:16` | No preserva query params en redirect |
| F22 | ⚪ BAJO | `entities/usuario-admin/api.ts:20-31` | Envía update como query params |

### Spec vs Código — fixes pendientes (8)

| # | Severidad | Archivo | Bug |
|---|-----------|---------|-----|
| S1 | 🟠 ALTO | `pedidos/fsm.py` | `_CANCEL_ROLES["EN_PREP"]` no incluye `PEDIDOS` |
| S2 | 🟠 ALTO | `pedidos/service.py` | Stock no se restaura al cancelar desde EN_PREP |
| S3 | 🟠 ALTO | `pedidos/fsm.py + service.py` | Sin RBAC para transiciones de avance (CLIENT puede avanzar) |
| S4 | 🔴 CRÍTICO | `auth/router.py` | `POST /logout` sin auth guard, status 200 en vez de 204 |
| S5 | 🟠 ALTO | `pedidos/router.py` | `PATCH /estado` usa `get_current_user` en vez de `require_role` |
| S6 | 🟠 ALTO | `admin/router.py` | `GET /metrics` permite STOCK y PEDIDOS (spec solo ADMIN) |
| S7 | 🟠 ALTO | `productos/router.py` | `POST /` permite STOCK (spec solo ADMIN) |
| S8 | 🟠 ALTO | `productos/router.py` | `PUT /{id}` permite STOCK (spec solo ADMIN) |

### Deuda técnica documentada (12 desviaciones intencionales)
Ver `tasks.md` para el detalle completo.

## Scope
- **Total fixes aplicados:** 29 (código) + 8 (spec) = 37
- **Archivos:** ~28 modificados (14 backend + 14 frontend)
- **Riesgo:** Medio — fixes puntuales, sin cambios de arquitectura
- **Dependencias:** Ninguna (independiente de otros changes)
