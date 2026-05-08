## ADDED Requirements

### Requirement: Auth errors displayed globally
The system SHALL display authentication errors as global notifications (toast).

#### Scenario: Login error displayed
- **WHEN** login fails with "Credenciales inválidas"
- **AND** a toast notification "Credenciales inválidas" is shown

#### Scenario: Registration error displayed
- **WHEN** registration fails with "El email ya existe"
- **AND** a toast notification "El email ya existe" is shown

### Requirement: Network errors displayed
The system SHALL display network errors (connection failed, timeout).

#### Scenario: Network error displayed
- **WHEN** API request fails due to network error
- **AND** a toast notification "Error de conexión. Intentalo más tarde." is shown

### Requirement: Session expired displayed
The system SHALL display a specific message when the session has expired.

#### Scenario: Session expired notification
- **WHEN** token refresh fails due to expired refresh token
- **AND** a toast notification "Tu sesión ha expirado. Por favor, volvés a ingresar." is shown
- **AND** user is redirected to /login

### Requirement: Unauthorized access message
The system SHALL display a message when user tries to access unauthorized resource.

#### Scenario: Unauthorized access
- **WHEN** user with role CLIENT tries to access /admin/dashboard
- **AND** a toast notification "No tenés acceso a esta sección" is shown

### Requirement: Toast auto-dismisses
The toast notifications SHALL auto-dismiss after a few seconds.

#### Scenario: Toast auto-dismiss
- **WHEN** a toast is shown
- **AND** after 5 seconds, the toast is automatically dismissed