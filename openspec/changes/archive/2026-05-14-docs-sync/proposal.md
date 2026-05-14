## Why

Durante code review de documentación se identificaron 9 inconsistencias críticas entre los documentos y el código real. Estas inconsistencias causan confusión en el equipo, pueden llevar a implementaciones incorrectas, y dificultan el onboarding de nuevos desarrolladores.

## What Changes

- Unificar formato de soft delete: `deleted_at` (ya usado en código) será el estándar en docs
- Unificar formato de estados FSM: `EN_PREP` (ya usado en código y tests) será el estándar
- Documentar módulo `sucursales` que existe en código pero no en docs
- Unificar endpoint de transición FSM: `/pedidos/{id}/estado` (ya usado en código) será el estándar
- Actualizar AUDITORIA-ROADMAP.md con estado actual (23 changes vs 18 documentados)
- Corregir ejemplos de código en CONTRIBUTING.md que no siguen el patrón documentado
- Unificar rate limiting en docs: `5/15minutes` (confirmado en código)

## Capabilities

### New Capabilities

- `sucursales-module`: Documentar el módulo de sucursales existente en `backend/app/modules/sucursales/`

### Modified Capabilities

- `soft-delete-field`: Unificar nombre del campo a `deleted_at` en todos los docs
- `fsm-states`: Unificar formato de estados FSM a `EN_PREP` (snake_case, sin tilde)
- `pedidos-endpoints`: Unificar endpoint de transición a `PATCH /api/v1/pedidos/{id}/estado`

## Impact

**Documentos a modificar:**
- `docs/Integrador.txt` — actualizar lista de módulos, soft delete field name, FSM states
- `docs/Descripcion.txt` — mismo sync que Integrador.txt
- `docs/Historias_de_usuario.txt` — actualizar RN-FS02, RN-PE02, RN-DI01 con naming correcto
- `docs/CHANGES-ROADMAP.md` — verificar estado de todos los 23 changes
- `docs/AUDITORIA-ROADMAP.md` — actualizar contador de changes y fecha
- `CONTRIBUTING.md` — corregir ejemplos de código que usan `with uow:` vs `async with uow:`