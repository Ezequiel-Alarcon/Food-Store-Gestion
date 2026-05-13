## ADDED Requirements

### Requirement: Gestor de Pedidos can list orders with pagination
The system MUST expose an authenticated endpoint to list orders with pagination metadata.

The endpoint MUST follow the global API convention:

- Base path prefix MUST be `/api/v1`.
- Pagination MUST use `page` and `size` query parameters.
- The response MUST include `{ items, total, page, size, pages }`.

#### Scenario: Default paginated listing
- **WHEN** a user with role `PEDIDOS` requests `GET /api/v1/pedidos?page=1&size=20`
- **THEN** the system returns HTTP 200 with a paginated response containing `items`, `total`, `page=1`, `size=20`, and `pages`

#### Scenario: Validation errors for pagination
- **WHEN** a user requests `GET /api/v1/pedidos?page=0&size=-1`
- **THEN** the system returns HTTP 422 with validation details

### Requirement: RBAC for order listing
The system MUST enforce RBAC for the orders listing endpoint.

- Users without a valid JWT MUST receive HTTP 401.
- Users with a valid JWT but without an allowed role MUST receive HTTP 403.
- Users with role `PEDIDOS` or `ADMIN` MUST be able to list ALL orders in the system.
- Users with role `CLIENT` MUST only be able to list their own orders (ownership by `user_id` from JWT).

#### Scenario: Unauthorized request
- **WHEN** a request is made to `GET /api/v1/pedidos` without a bearer token
- **THEN** the system returns HTTP 401

#### Scenario: Forbidden role
- **WHEN** a user with role `STOCK` requests `GET /api/v1/pedidos`
- **THEN** the system returns HTTP 403

#### Scenario: PEDIDOS sees all orders
- **WHEN** a user with role `PEDIDOS` requests `GET /api/v1/pedidos`
- **THEN** the system includes orders belonging to multiple users in `items`

#### Scenario: CLIENT sees only own orders
- **WHEN** a user with role `CLIENT` requests `GET /api/v1/pedidos`
- **THEN** every order in `items` has `user_id` equal to the authenticated user id

### Requirement: Operational filters for Gestor de Pedidos
The system MUST support operational filters for order listing via query parameters.

Supported filters:

- `estado` (optional): filter by order state code.
- `desde` (optional): filter orders with `created_at >= desde` (ISO 8601 datetime).
- `hasta` (optional): filter orders with `created_at <= hasta` (ISO 8601 datetime).
- `q` (optional): free-text search. For role `PEDIDOS`/`ADMIN`, it MUST match at least order id and customer email.

If any filter value is invalid (e.g., malformed datetime), the system MUST return HTTP 422.

#### Scenario: Filter by state
- **WHEN** a user with role `PEDIDOS` requests `GET /api/v1/pedidos?estado=CONFIRMADO&page=1&size=20`
- **THEN** every returned item has `estado_codigo = "CONFIRMADO"`

#### Scenario: Filter by date range
- **WHEN** a user with role `PEDIDOS` requests `GET /api/v1/pedidos?desde=2026-01-01T00:00:00Z&hasta=2026-01-31T23:59:59Z&page=1&size=20`
- **THEN** every returned item has `created_at` within the requested range

#### Scenario: Search by order id
- **WHEN** a user with role `PEDIDOS` requests `GET /api/v1/pedidos?q=12345&page=1&size=20`
- **THEN** the system returns only orders whose identifier matches the query

### Requirement: Sorting defaults for operational use
The system MUST define a deterministic default sort order for listings.

- Default ordering MUST be `created_at` descending (most recent first).
- An optional `orden` query parameter MAY be supported to switch ordering between `created_at_asc` and `created_at_desc`.

#### Scenario: Default ordering
- **WHEN** a user requests `GET /api/v1/pedidos?page=1&size=20`
- **THEN** the first item in `items` is the most recently created order

### Requirement: Response model for list items
The system MUST return a lightweight order representation suitable for operational listing.

Each item in `items` MUST include at least:

- `id`: integer
- `user_id`: integer (customer id)
- `estado_codigo`: string (one of: `PENDIENTE`, `CONFIRMADO`, `EN_PREP`, `EN_CAMINO`, `ENTREGADO`, `CANCELADO`)
- `total`: decimal serialized as string or number according to existing API conventions
- `created_at`: ISO 8601 datetime

For role `PEDIDOS`/`ADMIN`, each item MUST additionally include:

- `cliente_email`: string

#### Scenario: Minimal list item shape
- **WHEN** the system returns a paginated list response
- **THEN** every item includes `id`, `user_id`, `estado_codigo`, `total`, and `created_at`

#### Scenario: Operational fields for PEDIDOS
- **WHEN** a user with role `PEDIDOS` requests the listing
- **THEN** every item includes `cliente_email`

### Requirement: Error format consistency
The system MUST return errors in a consistent Problem Details style (RFC 7807 compatible) across the orders listing endpoint.

At minimum, error responses MUST include a human-readable `detail` and an HTTP status code aligned with the error.

#### Scenario: Forbidden response format
- **WHEN** a user with insufficient role requests `GET /api/v1/pedidos`
- **THEN** the system returns HTTP 403 and a JSON body containing `detail`
