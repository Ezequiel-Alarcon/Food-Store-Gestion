## ADDED Requirements

### Requirement: LoginForm displays correctly
The LoginForm component SHALL be rendered in the login page with email and password input fields, a submit button, and a link to the registration page.

#### Scenario: Initial render
- **WHEN** user navigates to /login
- **THEN** LoginForm is rendered with empty email and password fields, a "Ingresar" button, and a link to /register

### Requirement: LoginForm validates email
The LoginForm SHALL validate that the email field contains a valid email format before submission.

#### Scenario: Invalid email submitted
- **WHEN** user enters "invalid-email" in the email field and clicks submit
- **THEN** an error message "Email inválido" is displayed below the email field

### Requirement: LoginForm validates password
The LoginForm SHALL validate that the password field is not empty before submission.

#### Scenario: Empty password submitted
- **WHEN** user enters a valid email and leaves password empty, then clicks submit
- **AND** an error message "La contraseña es requerida" is displayed below the password field

### Requirement: LoginForm submits to login endpoint
The LoginForm SHALL make a POST request to /api/v1/auth/login with email and password when submitted.

#### Scenario: Valid credentials submitted
- **WHEN** user enters a valid email and password, then clicks "Ingresar"
- **THEN** the form makes a POST request to /api/v1/auth/login with { email, password }
- **AND** the submit button shows "Cargando..." and is disabled during the request

#### Scenario: Login successful
- **WHEN** the login API returns 200 with { accessToken, refreshToken, user }
- **THEN** the authStore is updated with the tokens and user
- **AND** the user is redirected to the home page or returnUrl

#### Scenario: Login failed with invalid credentials
- **WHEN** the login API returns 401 with { detail: "Credenciales inválidas" }
- **THEN** an error message "Credenciales inválidas" is displayed
- **AND** the form fields remain filled

### Requirement: LoginForm shows loading state
The LoginForm SHALL display a loading state while the login request is in progress.

#### Scenario: Loading during login
- **WHEN** the login request is pending
- **THEN** the submit button is disabled and shows "Cargando..."
- **AND** the form fields are disabled

### Requirement: LoginForm has link to register
The LoginForm SHALL include a link to the registration page.

#### Scenario: Navigate to register
- **WHEN** user clicks "¿No tenés cuenta? Registrate"
- **THEN** the user is navigated to /register