# Spec: intentional-deviations

> **Tipo:** Documentación de deuda técnica  
> **Origen:** Auditoría spec vs código (2026-05-18)  
> **Cambio padre:** `intentional-bug-recommendations`

## Resumen

Este spec documenta 12 desviaciones entre la especificación SDD v5.0 (`docs/Integrador.txt`) y el código implementado. Son desviaciones **intencionales** — decisiones de arquitectura o simplificaciones de MVP que el equipo decidió postergar como deuda técnica.

## Desviaciones

| # | Área | Descripción | Esfuerzo |
|---|------|-------------|----------|
| D1 | RBAC | UsuarioRol N:M no implementado (single rol field) | 3-4 días |
| D2 | Catálogo | FormaPago no existe (modelo, migración, seed) | 1-2 días |
| D3 | Seguridad | RefreshToken sin SHA-256 (JWT plano + revocado booleano) | 1 día |
| D4 | Pedidos | costo_envío = 0.0 (spec dice 50.00) | 0.5 días |
| D5 | Direcciones | UserAddress en vez de DireccionEntrega (naming inglés) | N/A |
| D6 | Auth | GET /auth/me → GET /perfil (módulo separado) | 0.5 días |
| D7 | Productos | activo+stock vs disponible+stock_cantidad; precio float vs DECIMAL | 1 día |
| D8 | Pedidos | DELETE /pedidos/{id} no existe (CLIENT no puede cancelar) | 1 día |
| D9 | Productos | PATCH /stock vs PATCH /disponibilidad (cantidad vs toggle) | 0.5 días |
| D10 | Core | SessionLocal bypass en admin/refreshtokens routers | 1 día |
| D11 | Auth | TokenResponse sin campo user (2 requests en vez de 1) | 0.5 días |
| D12 | Frontend | Rol GESTOR legacy en 7 archivos (spec v5.0: STOCK+PEDIDOS) | 1 día |

## Reglas de negocio afectadas

- **RN-RB01**: RBAC con 4 roles (afectado por D1 — single rol)
- **RN-PE03**: costo_envío fijo documentado (afectado por D4)
- **RN-FS08**: Cancelación por CLIENT desde PENDIENTE (afectado por D8)

## Referencias

- `docs/Integrador.txt` — Especificación SDD v5.0
- `openspec/changes/archive/2026-05-18-audit-bugfixes/` — 37 fixes aplicados (S1-S8)
- `openspec/changes/intentional-bug-recommendations/design.md` — Decisiones técnicas
