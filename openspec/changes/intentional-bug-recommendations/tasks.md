# Tasks: intentional-bug-recommendations

> **Objetivo:** Documentar las 12 desviaciones intencionales spec vs código identificadas en la auditoría del 2026-05-18.  
> **Tipo:** Change de documentación — NO se modifica código.  
> **Prerequisito:** `audit-bugfixes` completado (37 fixes aplicados, archivado 2026-05-18).

---

## 1. Documentación de desviaciones — Backend (D1-D10)

- [x] 1.1 D1 — Documentar decisión de RBAC simplificado (single `rol` vs tabla pivot UsuarioRol N:M). Archivos: `auth/model.py`, `core/deps.py`, `usuarios/model.py`.
- [x] 1.2 D2 — Documentar ausencia de entidad FormaPago. Archivos afectados: `pagos/model.py` (debería tener FormaPago), `db/seed.py` (debería seedear 3 registros), `pedidos/model.py` (debería tener FK forma_pago_codigo).
- [x] 1.3 D3 — Documentar almacenamiento de RefreshToken sin SHA-256. Archivos: `refreshtokens/model.py` (token plano + revocado booleano vs token_hash + revoked_at).
- [x] 1.4 D4 — Documentar costo_envío = 0.0 en vez de 50.00. Archivos: `pedidos/model.py:54`, `pedidos/service.py:155`.
- [x] 1.5 D5 — Documentar naming divergence en DireccionEntrega → UserAddress. Archivos: `direcciones/model.py` (UserAddress, etiqueta, is_default vs alias, linea1, es_principal).
- [x] 1.6 D6 — Documentar endpoint GET /auth/me movido a GET /perfil. Archivos: `auth/router.py` (sin /me), `perfil/router.py` (GET /perfil).
- [x] 1.7 D7 — Documentar divergencia de campos en Producto (activo vs disponible, stock vs stock_cantidad, precio float vs DECIMAL). Archivos: `productos/model.py`, `productos/schemas.py`.
- [x] 1.8 D8 — Documentar ausencia de DELETE /pedidos/{id} para cancelación de CLIENT. Archivos: `pedidos/router.py` (PATCH /estado con guard ADMIN+PEDIDOS bloquea CLIENT), `pedidos/fsm.py` (check_cancel_permission permite CLIENT desde PENDIENTE pero nunca se alcanza).
- [x] 1.9 D9 — Documentar PATCH /stock vs PATCH /disponibilidad. Archivos: `productos/router.py:267` (PATCH /{id}/stock actualiza cantidad, no toggle booleano).
- [x] 1.10 D10 — Documentar bypass de SessionLocal en routers admin y refreshtokens. Archivos: `admin/router.py:153,212`, `refreshtokens/router.py:51`.

## 2. Documentación de desviaciones — Frontend (D11-D12)

- [x] 2.1 D11 — Documentar TokenResponse sin campo `user`. Archivos: `auth/schemas.py` (backend, falta user en response), `stores/authStore.ts` (frontend hace 2 requests: login + /perfil).
- [x] 2.2 D12 — Documentar uso de rol `GESTOR` legacy en frontend. Archivos: `providers/RouterProvider.tsx:74,130`, `features/layout/Navigation.tsx:23`, `features/admin/users/ui/UsersPage.tsx:12`, `entities/usuario-admin/types.ts:8,22`.

## 3. Sincronización de documentación de tracking

- [x] 3.1 Actualizar `docs/CHANGES-ROADMAP.md`: corregir conteo de completados (34→39), marcar changes 40 y 41 como archivados, agregar `audit-bugfixes` como change #44, actualizar fecha.
- [x] 3.2 Actualizar `TEAM-ASSIGNMENT.md`: corregir resumen de Leandro (0 🔲 → 2 🔲), sync con cambios del roadmap.
- [x] 3.3 Marcar `AUDITORIA-ROADMAP.md` como OBSOLETO (analiza roadmap v1.0 de 15 cambios, abril 2026).
- [x] 3.4 Actualizar `AGENTS.md`: cambiar "22 cambios" por "43 cambios" en referencia a CHANGES-ROADMAP.md.

## 4. Verificación final

- [x] 4.1 Verificar que las 12 desviaciones estén correctamente referenciadas en proposal.md, design.md y specs/intentional-deviations/spec.md.
- [x] 4.2 Verificar que el link en `audit-bugfixes/tasks.md:61` apunte correctamente a `../intentional-bug-recommendations/tasks.md`.
- [x] 4.3 Ejecutar `openspec status --change "intentional-bug-recommendations"` y confirmar que todos los artifacts están done.
