## Context

El proyecto necesita un módulo de direcciones para dos casos de uso distintos:

- **Direcciones de usuario** (envíos): un usuario puede guardar **múltiples** direcciones y elegir una como **predeterminada**.
- **Direcciones de sucursal** (punto de retiro): una sucursal expone una dirección textual para mostrarse y seleccionarse como retiro.

El modelo será **texto** (sin geolocalización).

## Goals / Non-Goals

**Goals**
- CRUD de direcciones de usuario (crear/listar/editar/eliminar) y operación para marcar **predeterminada**.
- Garantizar que haya **a lo sumo 1** dirección predeterminada activa por usuario.
- CRUD de direcciones de sucursal (punto de retiro) y listado.
- Integración con RBAC:
  - usuario: solo gestiona sus direcciones
  - sucursales: gestión restringida (ADMIN u rol equivalente)

**Non-Goals**
- No lat/lng, no mapas, no validación/cálculo de distancia.
- No zonas de entrega.
- No normalización a tablas de “ciudad/provincia/país” (se guarda texto).

## Decisions

### 1) Dos tablas (user vs branch) en lugar de asociación polimórfica

**Decisión:** Modelar direcciones de usuario y direcciones de sucursal en **tablas separadas**.

**Alternativas consideradas:**
- **Tabla única** `addresses` con `owner_type` + `owner_id` (polimórfico).

**Rationale:** Simplifica integridad referencial (FKs reales), constraints (especialmente “una default por usuario”), queries, y permisos. El patrón polimórfico agrega complejidad innecesaria en SQLModel/SQLAlchemy.

### 2) “Una default por usuario” con constraint + lógica de servicio

**Decisión:** Implementar la regla con:
- **Constraint DB** (PostgreSQL): índice único parcial para `is_default = true` en direcciones activas.
- **Service layer**: en operación “set default”, ejecutar en una transacción (UoW) para desmarcar otras y marcar la nueva.

**Rationale:** El constraint evita estados inválidos por race conditions; el service mantiene la intención de negocio clara.

### 3) Soft-delete simple

**Decisión:** Usar flag `activa: bool` (true/false) para borrado lógico.

**Rationale:** Consultas simples y reversible; consistente con otros módulos del repo.

## Data Model (propuesto)

### user_addresses

- id: int (PK)
- user_id: int (FK usuarios)
- etiqueta: str | None ("Casa", "Trabajo")
- calle: str
- numero: str
- piso_depto: str | None
- ciudad: str
- provincia: str
- codigo_postal: str | None
- pais: str
- referencias: str | None
- is_default: bool
- activa: bool
- created_at / updated_at

**Constraint:** único parcial por usuario:
- `UNIQUE (user_id) WHERE is_default = true AND activa = true`

### branch_addresses

- id: int (PK)
- branch_id: int (FK sucursales)
- calle: str
- numero: str
- piso_depto: str | None
- ciudad: str
- provincia: str
- codigo_postal: str | None
- pais: str
- referencias: str | None
- activa: bool
- created_at / updated_at

**Constraint:** `UNIQUE (branch_id)` (una dirección activa principal por sucursal).

## API Surface (alto nivel)

> Nota: rutas exactas se fijan en specs.

**User**
- GET `/api/v1/user/addresses`
- POST `/api/v1/user/addresses`
- PATCH `/api/v1/user/addresses/{id}`
- DELETE `/api/v1/user/addresses/{id}` (soft-delete)
- POST `/api/v1/user/addresses/{id}/default`

**Branches**
- GET `/api/v1/branches/addresses` (listado)
- POST `/api/v1/branches/{branchId}/address`
- PATCH `/api/v1/branches/{branchId}/address`
- DELETE `/api/v1/branches/{branchId}/address` (soft-delete)

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Condición de carrera al setear default | Constraint único parcial + UoW transaccional |
| Reglas RBAC para sucursales no definidas | Especificar roles mínimos en specs y validar en deps |
| Duplicación de campos entre tablas | Aceptado por simplicidad; se puede refactorizar a value object más adelante |

## Migration Plan

1. Crear migraciones Alembic para `user_addresses` y `branch_addresses` + índices.
2. Implementar módulos backend (router/service/repo) siguiendo Router→Service→UoW→Repo.
3. Integrar frontend (perfil/checkout + admin sucursales) con store/query.
4. Añadir verificación manual (sin build/test, por restricción del repo).
