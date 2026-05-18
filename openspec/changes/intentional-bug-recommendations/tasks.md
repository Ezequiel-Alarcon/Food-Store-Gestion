# Tasks: intentional-bug-recommendations

> **Origen:** Auditoría spec vs código — `docs/Integrador.txt` vs implementación real  
> **Estado:** Solo documentación. Sin cambios de código en este change.

---

## 🔲 Endpoints faltantes o movidos

- [ ] D1. `GET /auth/me` no existe (está como `GET /perfil`)
  - **Spec:** `GET /api/v1/auth/me` con `UserResponse` y Bearer token
  - **Código:** `GET /api/v1/perfil` en `perfil/router.py`, retorna `dict` sin `response_model`
  - **Por qué se dejó:** Separación de dominio — perfil es su propio módulo feature-first
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** `auth-me-endpoint` — agregar el endpoint o documentar la divergencia en la spec

- [ ] D2. `DELETE /pedidos/{id}` absorbido en `PATCH /pedidos/{id}/estado`
  - **Spec:** `DELETE /api/v1/pedidos/{id}` para que CLIENT cancele su pedido (PENDIENTE o CONFIRMADO)
  - **Código:** La cancelación se hace via `PATCH /{id}/estado` con `{"nuevo_estado": "CANCELADO"}`
  - **Por qué se dejó:** Simplifica la API — un solo endpoint de transición para todos los cambios de estado
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** — (decisión de diseño, no requiere acción)

- [ ] D3. Endpoints de ingredientes en productos no existen
  - **Spec:** `GET/POST/DELETE /api/v1/productos/{id}/ingredientes[/{ing_id}]`
  - **Código:** No existen. La asociación producto-ingrediente se maneja en el POST/PUT del producto
  - **Por qué se dejó:** Scope — los ingredientes se gestionan inline en el CRUD de productos
  - **Prioridad:** 🟡 Media
  - **Change sugerido:** `productos-ingredientes-endpoints` — 3 endpoints nuevos en `productos/router.py`

- [ ] D4. `PATCH /productos/{id}/stock` vs spec `PATCH /productos/{id}/disponibilidad`
  - **Spec:** Toggle booleano `disponible: true/false`
  - **Código:** Gestión numérica de stock con operaciones `set|add|subtract` + valor numérico
  - **Por qué se dejó:** El equipo eligió gestión granular de stock (más útil que un toggle binario)
  - **Prioridad:** 🟡 Media
  - **Change sugerido:** `productos-disponibilidad-toggle` — agregar endpoint de toggle o actualizar la spec

- [ ] D5. Catálogo público en `/productos/catalogo`, no en `/productos`
  - **Spec:** `GET /api/v1/productos` debe ser catálogo público con filtros
  - **Código:** `GET /productos/catalogo` (público) y `GET /productos/` (admin-only)
  - **Por qué se dejó:** Evita colisión entre listado público y admin. Refactor más grande
  - **Prioridad:** 🟡 Media
  - **Change sugerido:** `productos-routes-refactor` — renombrar admin-list a `/admin/productos` y liberar `/productos`

- [ ] D6. Detalle público en `/{id}/publico`, no en `/{id}`
  - **Spec:** `GET /api/v1/productos/{id}` debe ser público
  - **Código:** `GET /{id}/publico` (público) y `GET /{id}` (admin-only)
  - **Por qué se dejó:** Misma razón que D5 — separación público/admin
  - **Prioridad:** 🟡 Media
  - **Change sugerido:** Incluir en `productos-routes-refactor`

---

## 🔲 Response models y status codes divergentes

- [ ] D7. `POST /auth/register` retorna `TokenResponse` en vez de `UserResponse`
  - **Spec:** `201 UserResponse`
  - **Código:** `201 TokenResponse` (con access_token, refresh_token)
  - **Por qué se dejó:** Decisión de UX — auto-login post-registro. El frontend espera tokens
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** — (decisión de UX, documentar divergencia en la spec)

- [ ] D8. `DELETE /productos/{id}` retorna 200 + body en vez de 204
  - **Spec:** `204 No Content` (sin body)
  - **Código:** `200 OK` con `{"message": "Producto eliminado correctamente"}`
  - **Por qué se dejó:** Cambio cosmético — el frontend no chequea el status code exacto
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** `productos-status-codes` — cambiar a 204 y quitar response_model

- [ ] D9. `GET /pedidos/{id}` response_model `PedidoRead` vs spec `PedidoDetail`
  - **Spec:** `PedidoDetail` (incluye items, historial, pago)
  - **Código:** `PedidoRead` (versión compacta, sin pago ni historial anidados)
  - **Por qué se dejó:** El frontend actual consume `PedidoRead`. Migrar a `PedidoDetail` requiere cambios en el frontend
  - **Prioridad:** 🟡 Media
  - **Change sugerido:** `pedidos-response-detail` — requiere coordinar backend + frontend

---

## 🔲 Funcionalidad no documentada en la spec

- [ ] D10. `POST /pagos/{id}/reintentar` no está en la spec
  - **Código:** Endpoint funcional en `pagos/router.py:94` para reintentar pago fallido
  - **Por qué se dejó:** Funcionalidad extra agregada por el equipo, útil para UX
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** — (funcionalidad extra, agregar a la spec o mantener como extensión)

- [ ] D11. `RegisterRequest` incluye `telefono` opcional (spec no lo pide)
  - **Spec:** `{ nombre, apellido, email, password }`
  - **Código:** `RegisterRequest` incluye `telefono: Optional[str]`
  - **Por qué se dejó:** Campo extra inofensivo, puede ser útil a futuro
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** — (campo extra, agregar a la spec o mantener)

- [ ] D12. Métricas auxiliares no en spec (`sales-chart`, `top-products`, `orders-by-status`)
  - **Código:** 3 endpoints extra en `admin/router.py` necesarios para gráficos recharts del frontend
  - **Por qué se dejó:** Endpoints de soporte requeridos por el dashboard frontend
  - **Prioridad:** 🟢 Baja
  - **Change sugerido:** — (endpoints de soporte, documentar en la spec)
