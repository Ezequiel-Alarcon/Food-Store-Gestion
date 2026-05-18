# Proposal: final-polish

## Why

La tercera re-auditoría encontró 2 bugs que afectan la demo: CLIENT no puede cancelar sus pedidos PENDIENTE (guard RBAC bloquea) y falta la ruta `/admin/pedidos` en el frontend (OrdersListPage importada pero sin usar). Son fixes de 1 línea cada uno.

## What Changes

- **B2 — CLIENT cancel:** Agregar `"CLIENT"` al `require_role` de `PATCH /api/v1/pedidos/{id}/estado` en `pedidos/router.py:102`.
- **F1 — Missing route:** Agregar ruta `/admin/pedidos` en `RouterProvider.tsx` antes de `/admin/pedidos/:id`.

## Impact

- **Archivos:** 2 (1 backend + 1 frontend)
- **Riesgo:** Bajo — fixes de 1 línea
