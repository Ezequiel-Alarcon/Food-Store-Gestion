## Requirements

### Requirement: User can manage multiple shipping addresses
El sistema SHALL permitir que un usuario autenticado gestione múltiples direcciones de envío propias, con borrado lógico.

#### Scenario: Create a new user address
- **WHEN** un usuario autenticado envía POST `/api/v1/user/addresses` con campos de dirección válidos
- **THEN** el sistema crea una dirección asociada al usuario (`user_id` = usuario actual)
- **AND** setea `activa: true`
- **AND** devuelve 201 con la dirección creada

#### Scenario: List active user addresses
- **WHEN** un usuario autenticado envía GET `/api/v1/user/addresses`
- **THEN** el sistema devuelve 200 con la lista de direcciones del usuario donde `activa: true`

#### Scenario: Update an existing user address
- **WHEN** un usuario autenticado envía PATCH `/api/v1/user/addresses/{id}`
- **AND** la dirección `{id}` existe, pertenece al usuario y está activa
- **THEN** el sistema actualiza solo los campos enviados
- **AND** devuelve 200 con la dirección actualizada

#### Scenario: Delete (soft-delete) a user address
- **WHEN** un usuario autenticado envía DELETE `/api/v1/user/addresses/{id}`
- **AND** la dirección `{id}` existe y pertenece al usuario
- **THEN** el sistema setea `activa: false`
- **AND** devuelve 204 No Content

#### Scenario: User tries to access another user's address
- **WHEN** un usuario autenticado intenta PATCH/DELETE sobre una dirección que no le pertenece
- **THEN** el sistema devuelve 403 Forbidden

---

### Requirement: User has at most one default active address
El sistema MUST garantizar que un usuario tenga como máximo **una** dirección predeterminada activa (`is_default = true` y `activa = true`).

#### Scenario: Set an address as default
- **WHEN** un usuario autenticado envía POST `/api/v1/user/addresses/{id}/default`
- **AND** la dirección `{id}` existe, pertenece al usuario y está activa
- **THEN** el sistema marca esa dirección como `is_default: true`
- **AND** desmarca cualquier otra dirección activa del mismo usuario (`is_default: false`)
- **AND** devuelve 200 con la dirección marcada como default

#### Scenario: Set default for a non-existent address
- **WHEN** un usuario autenticado envía POST `/api/v1/user/addresses/999999/default`
- **THEN** el sistema devuelve 404 Not Found

#### Scenario: Default address must be active
- **WHEN** un usuario autenticado intenta marcar como default una dirección con `activa: false`
- **THEN** el sistema devuelve 409 Conflict (o 400 Bad Request) indicando que la dirección no está activa

---

### Requirement: Address fields are textual and validated
El sistema SHALL validar que los campos de dirección sean textuales (sin lat/lng) y cumplan reglas mínimas.

#### Scenario: Minimal valid address
- **WHEN** se crea/actualiza una dirección con `calle`, `numero`, `ciudad`, `provincia`, `pais` no vacíos
- **THEN** el sistema acepta la operación

#### Scenario: Missing required fields
- **WHEN** se envía un request con `calle` vacío o faltante
- **THEN** el sistema devuelve 422 Unprocessable Entity (validación de Pydantic)
