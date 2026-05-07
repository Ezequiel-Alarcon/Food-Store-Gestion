## ADDED Requirements

### Requirement: Resolve current user from JWT
The system MUST provide a FastAPI dependency that resolves the current authenticated user from the incoming request's JWT.

#### Scenario: Authenticated request returns user
- **WHEN** a request includes a valid JWT for an existing user
- **THEN** the dependency MUST return that user as the current principal

#### Scenario: Missing or invalid token is rejected
- **WHEN** a request is missing a JWT or contains an invalid/expired JWT
- **THEN** the dependency MUST reject the request with an authentication error

### Requirement: Enforce role-based access
The system MUST provide a FastAPI dependency that enforces required role(s) for an endpoint.

#### Scenario: User with required role is allowed
- **WHEN** a request is made by an authenticated user whose role is in the required roles set
- **THEN** the dependency MUST allow the request to proceed

#### Scenario: User without required role is forbidden
- **WHEN** a request is made by an authenticated user whose role is not in the required roles set
- **THEN** the dependency MUST reject the request with an authorization error
