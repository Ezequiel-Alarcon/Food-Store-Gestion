## Why

Necesitamos un estándar único y reusable para acceso a datos y transacciones en el backend, para que los módulos (auth, productos, pedidos, etc.) puedan implementar reglas atómicas (commit/rollback) sin duplicación ni inconsistencias.

## What Changes

- Se introduce un **Unit of Work** (context manager) para manejar transacciones (commit/rollback) de forma explícita y consistente.
- Se introduce un **BaseRepository[T]** genérico para operaciones comunes (CRUD, queries básicas) y para reducir boilerplate por módulo.
- Se estandarizan **dependencias de autenticación/autorización** para FastAPI (`get_current_user`, `require_role`) para que el RBAC sea consistente en todos los routers.
- Se provee wiring base en `core/` para que Router → Service → UoW → Repository → Model sea el camino “feliz” por defecto.

## Capabilities

### New Capabilities
- `unit-of-work`: Patrón transaccional (context manager) para garantizar operaciones atómicas (commit/rollback) por request/caso de uso.
- `base-repository`: Repositorio genérico tipado para centralizar CRUD y helpers de persistencia.
- `auth-dependencies`: Dependencias FastAPI para resolver usuario actual y exigir roles (RBAC) de manera uniforme.

### Modified Capabilities
- (none)

## Impact

- Backend: `backend/app/core/` (nuevo/actualizado) y futuros módulos en `backend/app/modules/**` que consumirán UoW/Repo/Deps.
- Afecta el estilo de implementación: Services deben operar dentro de UoW y repositorios.
- No impacta frontend.
