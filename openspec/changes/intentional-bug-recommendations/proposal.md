# Proposal: intentional-bug-recommendations

## Why

La auditoría completa del proyecto (backend + frontend + docs vs spec SDD v5.0) realizada el 2026-05-18 reveló **71 hallazgos** entre los 3 frentes. De las 20 discrepancias spec vs código, 8 fueron arregladas en el change `audit-bugfixes` (S1-S8: FSM + guards de seguridad). Las **12 restantes (D1-D12)** son desviaciones intencionales — decisiones arquitectónicas, simplificaciones de MVP, o deuda técnica que requiere refactors mayores. Este change las documenta formalmente para que el equipo tenga visibilidad y pueda planificar su resolución.

## What Changes

- **D1 — RBAC: UsuarioRol N:M no implementado.** La spec define tabla pivot `UsuarioRol(usuario_id, rol_codigo)`. El código usa un solo campo `rol` en Usuario. Un usuario no puede tener múltiples roles simultáneamente.
- **D2 — FormaPago no existe.** La spec define catálogo `MERCADOPAGO | EFECTIVO | TRANSFERENCIA` con PK semántica. No hay modelo, migración ni seed en el código.
- **D3 — RefreshToken sin SHA-256.** La spec dice `token_hash CHAR(64)` (hash del JWT). El código guarda el JWT plano como `token` y usa `revocado` booleano en vez de `revoked_at TIMESTAMPTZ`.
- **D4 — costo_envío = 0 en vez de 50.** La spec define `DECIMAL(10,2) default 50.00`. El código hardcodea `0.0` en modelo y service.
- **D5 — DireccionEntrega → UserAddress.** La spec define `alias`, `linea1`, `es_principal`. El código usa `etiqueta`, `calle+numero`, `is_default`. Tablename `user_addresses`.
- **D6 — GET /auth/me → GET /perfil.** La spec define el endpoint en módulo auth. El código lo movió a módulo perfil separado (`GET /api/v1/perfil`).
- **D7 — Producto: `disponible` + `stock_cantidad` vs `activo` + `stock`.** La spec define toggle booleano independiente del stock. El código sobrecarga `activo` como soft-delete + disponibilidad, y `precio` es `float` en modelo (no `DECIMAL`).
- **D8 — DELETE /pedidos/{id} no existe.** La spec define cancelación de CLIENT vía DELETE. El código fusiona todo en PATCH /estado con guard `require_role("ADMIN","PEDIDOS")` que bloquea al CLIENT.
- **D9 — PATCH /disponibilidad → PATCH /stock.** La spec define toggle booleano. El código implementa actualización numérica de cantidad.
- **D10 — SessionLocal bypass en routers.** Los endpoints `GET /admin/pedidos/{id}/`, `GET /admin/pedidos/{id}/historial/` y `GET /refreshtokens/user/{user_id}` usan `SessionLocal()` directo, violando el patrón de inyección de dependencias.
- **D11 — TokenResponse sin campo `user`.** La spec dice que login/register deben devolver datos del usuario. El código solo devuelve tokens, forzando una request extra a `/perfil`.
- **D12 — Rol `GESTOR` legacy en frontend.** 7 archivos frontend referencian el rol `GESTOR` que no existe en la spec v5.0 (roles correctos: ADMIN, STOCK, PEDIDOS, CLIENT).

## Capabilities

### New Capabilities

Ninguna. Este change documenta deuda técnica existente, no introduce nuevas capacidades.

### Modified Capabilities

Ninguna. Los specs existentes no cambian — estas desviaciones se documentan tal cual están implementadas actualmente.

## Impact

- **Código afectado:** Ninguno directamente. Este es un change de documentación.
- **Dependencias:** Los cambios `audit-bugfixes` (37 fixes aplicados) es prerequisito — este change documenta lo que quedó pendiente.
- **Riesgo:** Bajo. No se modifica código.
