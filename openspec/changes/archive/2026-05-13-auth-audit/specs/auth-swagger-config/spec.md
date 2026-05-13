## ADDED Requirements

### Requirement: Swagger shows Bearer token input not OAuth2 form
The Swagger UI at /docs SHALL present a simple "Value" field for pasting a JWT Bearer token, instead of an OAuth2 password flow form with client_id/client_secret fields.

#### Scenario: Authorize button shows token input
- **WHEN** a developer opens /docs
- **THEN** the Authorize button opens a dialog with a single "Value" field for the Bearer token

#### Scenario: OAuth2 fields are absent
- **WHEN** a developer clicks Authorize in Swagger
- **THEN** no client_id, client_secret, or OAuth2 grant type fields are displayed

#### Scenario: Authenticated requests include Bearer token
- **WHEN** a developer enters a JWT in the Value field and authorizes
- **THEN** subsequent "Try it out" requests include the Authorization: Bearer header

### Requirement: Swagger auth uses HTTPBearer not OAuth2PasswordBearer
The FastAPI app MUST use HTTPBearer security scheme for extracting JWT tokens from requests, not OAuth2PasswordBearer.

#### Scenario: Token extraction from Authorization header
- **WHEN** a request includes Authorization: Bearer <token>
- **THEN** the dependency resolves the token correctly for get_current_user
