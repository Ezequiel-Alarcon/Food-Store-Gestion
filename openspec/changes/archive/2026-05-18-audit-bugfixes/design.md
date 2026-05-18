# Design: audit-bugfixes

## Approach

Fixes puntuales por archivo, organizados por prioridad. Sin cambios de arquitectura ni refactors grandes.

## Backend Fixes

### B1 — `total_usuarios` faltante
- **Archivo:** `admin/service.py`
- **Acción:** Agregar `data["total_usuarios"] = self.repo.get_total_usuarios_registrados()` antes de construir el response.
- **Repo:** Verificar que `admin/repository.py` tenga el método `get_total_usuarios_registrados()`. Si no existe, crearlo con `SELECT COUNT(*) FROM usuarios`.

### B2 — `.value` sobre `str`
- **Archivo:** `admin/router.py:231`
- **Acción:** Cambiar `h.actor_tipo.value` → `h.actor_tipo` (ya es string).

### B3 — Session leak
- **Archivo:** `admin/router.py:34-36`
- **Acción:** Reemplazar `_get_service()` que crea `SessionLocal()` directo por una dependencia que use `Depends(get_session)`.

### B4 — `from_attributes=True`
- **Archivo:** `usuarios/schemas.py`
- **Acción:** Agregar `model_config = ConfigDict(from_attributes=True)` en `UserRead` y `UserListResponse`.

### B5 — SQL injection CTE
- **Archivo:** `categorias/repository.py`
- **Acción:** Reemplazar f-strings por `:param` bind params en todas las queries CTE.

### B6 — FSM bypass
- **Archivo:** `pagos/service.py:282`
- **Acción:** Llamar `fsm.confirmar_pedido()` en lugar de duplicar validación.

### B7 — Código muerto
- **Archivo:** `productos/router.py:322`
- **Acción:** Eliminar línea `return None`.

### B8 — Tipo genérico
- **Archivo:** `productos/schemas.py:215`
- **Acción:** `items: list` → `items: list[Any]`.

### B9 — FormaPago muerto
- **Archivo:** `db/seed.py`
- **Acción:** Eliminar import `FormaPago` y función `seed_formas_pago()`.

### B10 — ImportError masking
- **Archivo:** `core/deps.py`
- **Acción:** Mover `session.get(Usuario, sub)` fuera del `try/except ImportError`.

### B11 — `list()` shadowing
- **Archivo:** `ingredientes/service.py`
- **Acción:** Renombrar método `list()` → `list_all()`.

### B12 — `float` para precio
- **Archivo:** `productos/schemas.py`
- **Acción:** Cambiar `precio: float` → `precio: Decimal` en todos los schemas.

### B13 — `actualizado_en` default
- **Archivo:** `ingredientes/model.py`
- **Acción:** Cambiar `default=None` → `default_factory=lambda: datetime.now(timezone.utc)`.

### B14 — Test metrics
- **Archivo:** `tests/modules/admin/test_admin_metrics.py`
- **Acción:** Actualizar test para esperar response correcto con `total_usuarios`.

### B15-B17 — Baja prioridad
- Cambios cosméticos o documentales. Documentados en tasks pero opcionales.

## Frontend Fixes

### F1 — `lib/api.ts` missing
- **Archivo:** CREAR `frontend/src/lib/api.ts`
- **Acción:** Crear el archivo con Axios instance + JWT interceptor. Basado en el código que existía antes de ser borrado (commit `1b71aee`).

### F2 — PaymentResult routes
- **Archivo:** `features/checkout/PaymentResult.tsx`
- **Acción:** Cambiar `navigate(\`/pedidos/${pedidoId}\`)` → `navigate('/pedidos')` (redirige a la lista).

### F3 — UsersPage pagination
- **Archivo:** `features/admin/users/ui/UsersPage.tsx:39,181-193`
- **Acción:** Agregar `setPage` al destructuring y usarlo en los botones.

### F4 — Hardcoded zeros
- **Archivo:** `features/admin/orders/ui/OrderDetailPage.tsx`
- **Acción:** Pasar `costo_envio` y `total` como props adicionales a `OrderItemsList`.

### F5-F6 — paymentStore
- **Archivo:** `stores/paymentStore.ts`
- **Acción:** Mover `get()` antes de `set()` en `startCheckout`. Agregar `pedidoId` al estado.

### F7 — DashboardPage FSD violation
- **Archivo:** `features/admin/dashboard/DashboardPage.tsx`
- **Acción:** Eliminar wrapper `ProtectedRoute` (el router ya protege la ruta).

### F8 — LoginForm return URL
- **Archivo:** `features/auth/LoginForm.tsx`
- **Acción:** Leer `location.state?.from` y navegar ahí en vez de siempre `/`.

### F9-F22 — Resto de bugs
- Documentados en tasks. Prioridad media-baja.
