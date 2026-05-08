## ADDED Requirements

### Requirement: ProtectedRoute redirects to login when not authenticated
The ProtectedRoute component SHALL redirect unauthenticated users to /login.

#### Scenario: User without accessToken tries to access protected route
- **WHEN** user navigates to /pedidos without being authenticated (no accessToken in store)
- **THEN** the user is redirected to /login?returnUrl=/pedidos

### Requirement: ProtectedRoute allows authenticated users
The ProtectedRoute component SHALL allow authenticated users to access the protected content.

#### Scenario: Authenticated user accesses protected route
- **WHEN** user with valid accessToken navigates to /pedidos
- **THEN** the protected content is rendered

### Requirement: ProtectedRoute checks roles
The ProtectedRoute component SHALL verify that the user has one of the required roles when roles are specified.

#### Scenario: User lacks required role
- **WHEN** user with role CLIENT tries to access /admin/dashboard (requires ADMIN role)
- **AND** the user is redirected to /unauthorized or home page

### Requirement: ProtectedRoute preserves returnUrl
The ProtectedRoute component SHALL preserve the original URL for redirect after successful login.

#### Scenario: User redirected to login, then logs in
- **WHEN** unauthenticated user tries to access /pedidos, is redirected to /login?returnUrl=/pedidos
- **AND** after successful login, the user is redirected back to /pedidos