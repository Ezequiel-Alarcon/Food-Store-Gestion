## ADDED Requirements

### Requirement: Category CRUD Operations
The system SHALL provide CRUD operations for categories with soft-delete semantics. All operations require authentication (ADMIN or GERENTE role).

#### Scenario: Create root category
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `nombre: "Comidas"`, `padre_id: null`
- **THEN** system creates category with `id` assigned, `slug` auto-generated as "comidas", `padre_id: null`, `activa: true`
- **AND** returns 201 with full category data including timestamps

#### Scenario: Create child category
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `nombre: "Italiana"`, `padre_id: 1`
- **AND** category with id=1 exists and is active
- **THEN** system creates category with `padre_id: 1`
- **AND** returns 201

#### Scenario: Create category with duplicate name at same level
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `nombre: "Italiana"`, `padre_id: 1`
- **AND** category "Italiana" already exists under padre_id=1
- **THEN** system returns 409 Conflict
- **AND** error message indicates duplicate name constraint

#### Scenario: Create category with invalid parent
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `padre_id: 9999`
- **AND** category with id=9999 does not exist
- **THEN** system returns 404 Not Found
- **AND** error message indicates parent not found

#### Scenario: List all active categories
- **WHEN** authenticated user sends GET `/api/v1/categorias/`
- **THEN** system returns 200 with list of all categories where `activa: true`
- **AND** each category includes `id`, `nombre`, `slug`, `descripcion`, `padre_id`, `orden`

#### Scenario: Get single category
- **WHEN** authenticated user sends GET `/api/v1/categorias/1`
- **AND** category with id=1 exists and is active
- **THEN** system returns 200 with full category data including `created_at`, `updated_at`

#### Scenario: Get non-existent category
- **WHEN** authenticated user sends GET `/api/v1/categorias/9999`
- **THEN** system returns 404 Not Found

#### Scenario: Update category
- **WHEN** authenticated ADMIN sends PUT `/api/v1/categorias/1` with `nombre: "Comidas Actualizado"`
- **AND** category with id=1 exists and is active
- **THEN** system updates `nombre`, `slug`, and `updated_at`
- **AND** returns 200 with updated data

#### Scenario: Soft delete category
- **WHEN** authenticated ADMIN sends DELETE `/api/v1/categorias/1`
- **AND** category with id=1 exists
- **THEN** system sets `activa: false`, `updated_at` to current time
- **AND** returns 204 No Content
- **AND** subsequent GET returns 404

#### Scenario: Delete category with children
- **WHEN** authenticated ADMIN sends DELETE `/api/v1/categorias/1`
- **AND** category with id=1 has active children
- **THEN** system soft-deletes all descendant categories recursively
- **AND** returns 204 No Content

---

### Requirement: Category Name Validation
The system SHALL enforce unique names among sibling categories (same parent) and validate name format.

#### Scenario: Valid category name
- **WHEN** creating category with `nombre: "Pizzas"`, `descripcion: "Platos de pizza"`
- **THEN** system accepts names up to 100 characters
- **AND** accepts alphanumeric, spaces, and common punctuation

#### Scenario: Invalid empty name
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `nombre: ""`
- **THEN** system returns 422 Unprocessable Entity
- **AND** error indicates required field

#### Scenario: Name too long
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `nombre: "A" * 101`
- **THEN** system returns 422 Unprocessable Entity
- **AND** error indicates max length constraint

#### Scenario: Slug auto-generation
- **WHEN** creating category with `nombre: "Comidas Italianas"`
- **THEN** system auto-generates `slug: "comidas-italianas"`
- **AND** slug is unique across all categories
- **AND** special characters are removed/replaced (á→a, é→e, etc.)
- **AND** spaces become hyphens