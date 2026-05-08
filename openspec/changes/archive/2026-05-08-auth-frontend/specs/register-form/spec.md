## ADDED Requirements

### Requirement: RegisterForm displays correctly
The RegisterForm component SHALL be rendered in the registration page with name, email, password, and confirm password fields, a submit button, and a link to the login page.

#### Scenario: Initial render
- **WHEN** user navigates to /register
- **THEN** RegisterForm is rendered with name, email, password, confirm password fields, a "Registrarse" button, and a link to /login

### Requirement: RegisterForm validates name
The RegisterForm SHALL validate that the name field is not empty before submission.

#### Scenario: Empty name submitted
- **WHEN** user leaves the name field empty and clicks submit
- **THEN** an error message "El nombre es requerido" is displayed below the name field

### Requirement: RegisterForm validates email
The RegisterForm SHALL validate that the email field contains a valid email format before submission.

#### Scenario: Invalid email submitted
- **WHEN** user enters "invalid-email" in the email field and clicks submit
- **THEN** an error message "Email inválido" is displayed below the email field

### Requirement: RegisterForm validates password
The RegisterForm SHALL validate that the password field is at least 8 characters.

#### Scenario: Short password submitted
- **WHEN** user enters a password with less than 8 characters and clicks submit
- **THEN** an error message "La contraseña debe tener al menos 8 caracteres" is displayed

### Requirement: RegisterForm validates password match
The RegisterForm SHALL validate that password and confirm password fields match.

#### Scenario: Passwords do not match
- **WHEN** user enters "password123" in password and "password456" in confirm password, then clicks submit
- **AND** an error message "Las contraseñas no coinciden" is displayed

### Requirement: RegisterForm submits to register endpoint
The RegisterForm SHALL make a POST request to /api/v1/auth/register with nombre, email, and password when submitted.

#### Scenario: Valid data submitted
- **WHEN** user enters valid name, email, password, confirms password, then clicks "Registrarse"
- **THEN** the form makes a POST request to /api/v1/auth/register with { nombre, email, password }
- **AND** the submit button shows "Cargando..." and is disabled during the request

#### Scenario: Registration successful
- **WHEN** the register API returns 201 with { accessToken, refreshToken, user }
- **THEN** the authStore is updated with the tokens and user
- **AND** the user is redirected to the home page

#### Scenario: Registration failed with existing email
- **WHEN** the register API returns 400 with { detail: "El email ya existe" }
- **AND** an error message "El email ya existe" is displayed

### Requirement: RegisterForm shows loading state
The RegisterForm SHALL display a loading state while the registration request is in progress.

#### Scenario: Loading during registration
- **WHEN** the registration request is pending
- **THEN** the submit button is disabled and shows "Cargando..."
- **AND** the form fields are disabled

### Requirement: RegisterForm has link to login
The RegisterForm SHALL include a link to the login page.

#### Scenario: Navigate to login
- **WHEN** user clicks "¿Ya tenés cuenta? Ingresá"
- **THEN** the user is navigated to /login