## Requirements

### Requirement: Branch pickup addresses can be listed
El sistema SHALL exponer direcciones de sucursales (puntos de retiro) para que el cliente pueda verlas/seleccionarlas.

#### Scenario: List active branch pickup addresses
- **WHEN** un usuario (autenticado o público, según configuración del router) envía GET `/api/v1/branches/addresses`
- **THEN** el sistema devuelve 200 con la lista de direcciones activas de sucursales
- **AND** cada item incluye `branch_id` y los campos textuales de dirección

---

### Requirement: Admin can manage branch pickup addresses
El sistema SHALL permitir que un usuario con rol ADMIN (o rol de gestión equivalente) gestione la dirección de una sucursal.

#### Scenario: Create branch address
- **WHEN** un ADMIN envía POST `/api/v1/branches/{branchId}/address` con campos válidos
- **THEN** el sistema crea/establece la dirección activa para esa sucursal
- **AND** devuelve 201 con la dirección

#### Scenario: Update branch address
- **WHEN** un ADMIN envía PATCH `/api/v1/branches/{branchId}/address`
- **AND** existe una dirección activa para `{branchId}`
- **THEN** el sistema actualiza los campos enviados
- **AND** devuelve 200

#### Scenario: Soft-delete branch address
- **WHEN** un ADMIN envía DELETE `/api/v1/branches/{branchId}/address`
- **THEN** el sistema marca `activa: false`
- **AND** devuelve 204

#### Scenario: Non-admin tries to manage branch address
- **WHEN** un usuario sin rol ADMIN intenta POST/PATCH/DELETE sobre `/api/v1/branches/{branchId}/address`
- **THEN** el sistema devuelve 403 Forbidden

---

### Requirement: Branch has at most one active pickup address
El sistema MUST garantizar que una sucursal tenga como máximo una dirección activa principal.

#### Scenario: Create address when one already exists
- **WHEN** un ADMIN intenta crear una dirección para una sucursal que ya tiene una dirección activa
- **THEN** el sistema reemplaza la existente (soft-delete de la anterior) o devuelve 409 Conflict
- **AND** el comportamiento elegido MUST estar documentado en el diseño/implementación
