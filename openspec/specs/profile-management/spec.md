## ADDED Requirements

### Requirement: View own profile
The frontend SHALL display the authenticated user's profile data fetched from `GET /api/v1/perfil`, including: id, nombre, apellido, email, rol, telefono.

#### Scenario: Authenticated user views profile page
- **WHEN** an authenticated user navigates to `/perfil`
- **THEN** the system displays their current profile data (nombre, apellido, email, rol, teléfono) in a read-only card

#### Scenario: Profile data loads with loading state
- **WHEN** the profile data is being fetched from the API
- **THEN** the system displays a loading indicator

#### Scenario: Profile fetch fails
- **WHEN** the `GET /api/v1/perfil` request fails (network error, 401, etc.)
- **THEN** the system displays an error message with a retry option

### Requirement: Edit own profile
The frontend SHALL allow the authenticated user to update their nombre, apellido, and teléfono via `PUT /api/v1/perfil`.

#### Scenario: User updates profile fields
- **WHEN** the user modifies nombre, apellido, and/or teléfono and submits the form
- **THEN** the system sends `PUT /api/v1/perfil` with the changed fields, displays a success message, and refreshes the displayed profile data

#### Scenario: Update fails with validation error
- **WHEN** the `PUT /api/v1/perfil` request returns a validation error (422)
- **THEN** the system displays the error details inline on the form fields

#### Scenario: Update fails with server error
- **WHEN** the `PUT /api/v1/perfil` request fails with a 5xx error
- **THEN** the system displays a generic error message

### Requirement: Change password
The frontend SHALL allow the authenticated user to change their password via `PUT /api/v1/perfil/password`.

#### Scenario: User changes password successfully
- **WHEN** the user enters their current password and a new password (min 8 chars), and submits the form
- **THEN** the system sends `PUT /api/v1/perfil/password`, displays a success message, and clears the form

#### Scenario: Current password is incorrect
- **WHEN** the `PUT /api/v1/perfil/password` request returns a 401 error (current password incorrect)
- **THEN** the system displays an error message "Contraseña actual incorrecta" on the current password field

#### Scenario: New password is same as current
- **WHEN** the `PUT /api/v1/perfil/password` request returns a 400 error (new password equals current)
- **THEN** the system displays an error message "La nueva contraseña no puede ser igual a la actual"

#### Scenario: Password change forces re-authentication
- **WHEN** the password is changed successfully and subsequent API calls fail with 401 (refresh tokens invalidated)
- **THEN** the system's Axios interceptor handles the 401 by attempting refresh, which fails, triggering logout and redirect to `/login`

### Requirement: Navigation access to profile
The frontend SHALL provide access to the profile page through the main navigation and routing.

#### Scenario: Client user sees profile link in navigation
- **WHEN** a user with role CLIENT is authenticated
- **THEN** the navigation bar displays a "Mi Perfil" link pointing to `/perfil`

#### Scenario: Profile route is protected
- **WHEN** an unauthenticated user navigates to `/perfil`
- **THEN** the system redirects them to `/login`

#### Scenario: Profile route accessible to all authenticated roles
- **WHEN** any authenticated user (CLIENT, ADMIN, STOCK, PEDIDOS, GESTOR) navigates to `/perfil`
- **THEN** the system displays the ProfilePage
