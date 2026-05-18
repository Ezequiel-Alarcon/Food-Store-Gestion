## MODIFIED Requirements

### Requirement: Admin can manage branch pickup addresses
El sistema SHALL permitir que un usuario con rol ADMIN gestione la dirección de una sucursal tanto desde la API como desde la UI de administración en `/admin/sucursales`.

#### Scenario: Create branch address via API
- **WHEN** un ADMIN envía POST `/api/v1/branches/{branchId}/address` con campos válidos
- **THEN** el sistema crea/establece la dirección activa para esa sucursal
- **AND** devuelve 201 con la dirección

#### Scenario: Update branch address via API
- **WHEN** un ADMIN envía PATCH `/api/v1/branches/{branchId}/address`
- **AND** existe una dirección activa para `{branchId}`
- **THEN** el sistema actualiza los campos enviados
- **AND** devuelve 200

#### Scenario: Soft-delete branch address via API
- **WHEN** un ADMIN envía DELETE `/api/v1/branches/{branchId}/address`
- **THEN** el sistema marca `activa: false`
- **AND** devuelve 204

#### Scenario: Non-admin tries to manage branch address
- **WHEN** un usuario sin rol ADMIN intenta POST/PATCH/DELETE sobre `/api/v1/branches/{branchId}/address`
- **THEN** el sistema devuelve 403 Forbidden

#### Scenario: Admin manages branch address from admin UI
- **WHEN** un ADMIN crea o edita una sucursal desde `/admin/sucursales`
- **THEN** el sistema permite ingresar/editar los campos de dirección (calle, número, ciudad, provincia, país, CP, referencias)
- **AND** los cambios se persisten via POST/PATCH a `/api/v1/branches/{branchId}/address`
