## ADDED Requirements

### Requirement: Admin Orders List Page
The system SHALL provide a orders management page at `/admin/pedidos` accessible only to ADMIN and GESTOR_PEDIDOS roles.

#### Scenario: Page loads with orders
- **WHEN** a user with ADMIN or GESTOR_PEDIDOS role navigates to `/admin/pedidos`
- **THEN** the system displays a table with all orders
- **AND** columns: ID, Cliente, Fecha, Estado, Total, Acciones
- **AND** data is fetched from `GET /api/v1/admin/pedidos`

#### Scenario: Filter by status
- **WHEN** a user selects a status filter (e.g., "EN_PREP")
- **THEN** the table updates to show only orders with that status
- **AND** the filter is reflected in the URL query params

#### Scenario: Search by client name
- **WHEN** a user types in the search input
- **THEN** the table filters to show orders from clients whose names contain the search term

#### Scenario: Pagination
- **WHEN** there are more than 20 orders
- **THEN** the system displays pagination controls
- **AND** each page shows 20 orders

#### Scenario: Empty results
- **WHEN** no orders match the current filters
- **THEN** the system displays "No se encontraron pedidos" message

### Requirement: Order Detail Page
The system SHALL provide a detailed view of an order at `/admin/pedidos/:id`.

#### Scenario: Load order detail
- **WHEN** a user navigates to `/admin/pedidos/{orderId}`
- **THEN** the system displays: order ID, client info, delivery address, items list, total amount, payment status, current state
- **AND** a timeline showing all state transitions with timestamps

#### Scenario: State timeline display
- **WHEN** viewing order detail
- **THEN** the system displays a vertical timeline with: state name, transition date/time, and elapsed time since each transition

#### Scenario: Order not found
- **WHEN** the order ID does not exist or is not accessible
- **THEN** the system displays a 404 message with a link back to the list

### Requirement: Status Badge Colors
Each order status SHALL have a visual indicator with specific colors.

- PENDIENTE: badge yellow
- CONFIRMADO: badge blue
- EN_PREP: badge purple
- EN_CAMINO: badge indigo
- ENTREGADO: badge green
- CANCELADO: badge red

### Requirement: Loading and Error States
The system SHALL provide appropriate feedback during data fetching and error scenarios.

#### Scenario: Loading state
- **WHEN** fetching orders
- **THEN** skeleton loaders are displayed in place of the table

#### Scenario: Error state
- **WHEN** the API request fails
- **THEN** an error message is displayed with a "Reintentar" button