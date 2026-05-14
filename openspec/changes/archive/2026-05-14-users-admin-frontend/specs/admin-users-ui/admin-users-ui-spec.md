## ADDED Requirements

### Requirement: Admin Users List Page
The system SHALL provide a users management page at `/admin/usuarios` accessible only to ADMIN role.

#### Scenario: Page loads with users
- **WHEN** an ADMIN navigates to `/admin/usuarios`
- **THEN** the system displays a table with all users
- **AND** columns: Nombre, Email, Rol, Estado, Fecha de Registro, Acciones
- **AND** data is fetched from `GET /api/v1/usuarios`

#### Scenario: Search by name or email
- **WHEN** ADMIN types in the search input
- **THEN** the table filters to show users whose name or email contains the search term (case-insensitive)

#### Scenario: Filter by role
- **WHEN** ADMIN selects a role in the filter dropdown
- **THEN** the table shows only users with that role

#### Scenario: Pagination
- **WHEN** there are more than 20 users
- **THEN** the system displays pagination controls
- **AND** each page shows 20 users

#### Scenario: Empty results
- **WHEN** no users match the current filters
- **THEN** the system displays "No se encontraron usuarios" message

#### Scenario: Loading state
- **WHEN** fetching users
- **THEN** skeleton loaders are displayed in place of the table

#### Scenario: Error state
- **WHEN** the API request fails
- **THEN** an error message is displayed with a "Reintentar" button

### Requirement: Edit User Role
The system SHALL allow ADMIN to edit the role of any user via a modal dialog.

#### Scenario: Open edit modal
- **WHEN** ADMIN clicks the edit button on a user row
- **THEN** a modal opens with the user's current role selected in a dropdown
- **AND** the dropdown shows all available roles: ADMIN, STOCK, PEDIDOS, CLIENT

#### Scenario: Save role change
- **WHEN** ADMIN selects a new role and clicks "Guardar"
- **THEN** the system sends `PUT /api/v1/usuarios/:id` with the new role
- **AND** on success, the table updates and the modal closes
- **AND** a success toast is shown

#### Scenario: Last ADMIN protection
- **WHEN** ADMIN tries to change the role of the last ADMIN in the system
- **THEN** the system displays a warning message
- **AND** the save button is disabled or the request is blocked by the backend

#### Scenario: Cancel edit
- **WHEN** ADMIN clicks "Cancelar" in the edit modal
- **THEN** the modal closes without sending any request

### Requirement: Toggle User Active Status
The system SHALL allow ADMIN to activate or deactivate any user.

#### Scenario: Deactivate user
- **WHEN** ADMIN clicks the deactivate button on an active user
- **THEN** the system sends `PATCH /api/v1/usuarios/:id/estado` with `activo: false`
- **AND** on success, the user status updates and a toast confirms it

#### Scenario: Activate user
- **WHEN** ADMIN clicks the activate button on an inactive user
- **THEN** the system sends `PATCH /api/v1/usuarios/:id/estado` with `activo: true`
- **AND** on success, the user status updates and a toast confirms it

#### Scenario: Cannot deactivate self as last ADMIN
- **WHEN** ADMIN is the last active ADMIN and tries to deactivate themselves
- **THEN** the system shows an error: "No puedes desactivar tu cuenta si eres el último administrador"

### Requirement: Navigation Update
The system SHALL show the "Gestión de Usuarios" link in the ADMIN navigation menu.

#### Scenario: ADMIN sees users management link
- **WHEN** a user with ADMIN role is logged in
- **THEN** the navigation shows "Gestión de Usuarios" link pointing to `/admin/usuarios`