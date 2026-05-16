## ADDED Requirements

### Requirement: Datetime timezone-aware migration

All datetime assignments in backend modules SHALL use `datetime.now(timezone.utc)` instead of `datetime.utcnow()` to produce timezone-aware datetimes.

**Rationale:** `datetime.utcnow()` was deprecated in Python 3.12 because it returns a naive datetime that Python treats as ambiguous. `datetime.now(timezone.utc)` returns a timezone-aware datetime, eliminating ambiguity in comparisons and JSON serialization.

#### Scenario: producto service updates timestamp
- **WHEN** `ProductoService` updates a producto's `actualizado_en`
- **THEN** the value is set using `datetime.now(timezone.utc)`

#### Scenario: producto repository soft-deletes producto
- **WHEN** `ProductoRepository` soft-deletes a producto
- **THEN** `eliminado_en` is set using `datetime.now(timezone.utc)`

#### Scenario: sucursales service creates entity
- **WHEN** `SucursalService` creates a new sucursal with `created_at` and `updated_at`
- **THEN** both fields use `datetime.now(timezone.utc)`

#### Scenario: direcciones service updates address
- **WHEN** `DireccionService` updates an address's `updated_at`
- **THEN** the value is set using `datetime.now(timezone.utc)`

#### Scenario: direcciones service creates address
- **WHEN** `DireccionService` creates a new direccion with `created_at` and `updated_at`
- **THEN** both fields use `datetime.now(timezone.utc)`