## ADDED Requirements

### Requirement: Ingredient CRUD Operations
The system SHALL provide CRUD operations for ingredients with soft-delete semantics. All write operations require authentication (ADMIN or STOCK role). Read operations are allowed for all authenticated roles.

#### Scenario: Create ingredient
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `nombre: "Harina de trigo"`, `descripcion: "Base para panes y pizzas"`, `es_alergeno: true`
- **THEN** system creates ingredient with `id` assigned, `nombre: "Harina de trigo"`, `descripcion: "Base para panes y pizzas"`, `es_alergeno: true`
- **AND** returns 201 with full ingredient data including `creado_en`

#### Scenario: Create ingredient with minimal data
- **WHEN** authenticated STOCK sends POST `/api/v1/ingredientes/` with `nombre: "Sal"`, `es_alergeno: false`
- **THEN** system creates ingredient with auto-generated id
- **AND** returns 201

#### Scenario: Create ingredient with duplicate name
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `nombre: "Sal"`
- **AND** ingredient "Sal" already exists and is not soft-deleted
- **THEN** system returns 409 Conflict
- **AND** error message indicates duplicate name constraint

#### Scenario: List all active ingredients
- **WHEN** authenticated user sends GET `/api/v1/ingredientes/`
- **THEN** system returns 200 with list of all ingredients where `eliminado_en IS NULL`
- **AND** each ingredient includes `id`, `nombre`, `descripcion`, `es_alergeno`, `creado_en`, `actualizado_en`
- **AND** results are paginated with default limit 20

#### Scenario: List ingredients filtered by allergen
- **WHEN** authenticated user sends GET `/api/v1/ingredientes/?es_alergeno=true`
- **THEN** system returns 200 with only ingredients where `es_alergeno = true`

#### Scenario: Get single ingredient
- **WHEN** authenticated user sends GET `/api/v1/ingredientes/1`
- **AND** ingredient with id=1 exists and is not soft-deleted
- **THEN** system returns 200 with full ingredient data

#### Scenario: Get non-existent ingredient
- **WHEN** authenticated user sends GET `/api/v1/ingredientes/9999`
- **THEN** system returns 404 Not Found

#### Scenario: Update ingredient
- **WHEN** authenticated ADMIN sends PATCH `/api/v1/ingredientes/1` with `nombre: "Harina integral"`, `es_alergeno: false`
- **AND** ingredient with id=1 exists and is not soft-deleted
- **THEN** system updates `nombre`, `descripcion` (if provided), `es_alergeno`, and `actualizado_en`
- **AND** returns 200 with updated data

#### Scenario: Soft delete ingredient
- **WHEN** authenticated STOCK sends DELETE `/api/v1/ingredientes/1`
- **AND** ingredient with id=1 exists
- **THEN** system sets `eliminado_en` to current timestamp
- **AND** returns 204 No Content
- **AND** subsequent GET returns 404

#### Scenario: Create ingredient without name
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `nombre: ""`
- **THEN** system returns 422 Unprocessable Entity
- **AND** error indicates required field

#### Scenario: Create ingredient with name too long
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `nombre: "A" * 101`
- **THEN** system returns 422 Unprocessable Entity
- **AND** error indicates max length constraint

#### Scenario: Create ingredient with invalid es_alergeno value
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `es_alergeno: "yes"`
- **THEN** system returns 422 Unprocessable Entity

---

### Requirement: Ingredient Name Uniqueness
The system SHALL enforce unique ingredient names among non-deleted ingredients.

#### Scenario: Create ingredient with same name as deleted one
- **WHEN** authenticated ADMIN sends POST `/api/v1/ingredientes/` with `nombre: "Sal"`
- **AND** ingredient "Sal" exists but was soft-deleted (`eliminado_en` is not null)
- **THEN** system creates ingredient successfully
- **AND** returns 201

#### Scenario: List ingredients exclude soft-deleted
- **WHEN** authenticated user sends GET `/api/v1/ingredientes/`
- **THEN** system returns only ingredients where `eliminado_en IS NULL`
- **AND** previously deleted ingredients are not visible

---

### Requirement: Ingredient Data Validation
The system SHALL validate ingredient data according to defined constraints.

#### Scenario: Valid ingredient with description
- **WHEN** creating ingredient with `nombre: "Queso mozzarella"`, `descripcion: "Queso italiano típico"`, `es_alergeno: true`
- **THEN** system accepts names up to 100 characters
- **AND** accepts descriptions up to 500 characters

#### Scenario: Description too long
- **WHEN** authenticated ADMIN sends PATCH `/api/v1/ingredientes/1` with `descripcion: "A" * 501`
- **THEN** system returns 422 Unprocessable Entity
- **AND** error indicates max length constraint

#### Scenario: Name exactly at limit
- **WHEN** creating ingredient with `nombre: "A" * 100`
- **THEN** system accepts the name as valid