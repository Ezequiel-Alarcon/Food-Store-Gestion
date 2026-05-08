## ADDED Requirements

### Requirement: User can refresh access token
El sistema SHALL permitir la renovación del access_token usando un refresh_token válido.

#### Scenario: Successful token refresh
- **WHEN** el usuario envía POST /api/v1/auth/refresh con refresh_token válido
- **THEN** el sistema invalida el refresh_token usado y devuelve un nuevo access_token y un nuevo refresh_token (token rotation)

#### Scenario: Refresh with expired refresh token
- **WHEN** el usuario envía un refresh_token expirado (más de 7 días)
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Refresh token expirado"

#### Scenario: Refresh with invalid token
- **WHEN** el usuario envía un refresh_token que no existe en la base de datos
- **THEN** el sistema devuelve error 401 Unauthorized

### Requirement: Refresh tokens must be rotated on use
El sistema MUST generar un nuevo refresh_token cada vez que se usa uno válido (token rotation).

#### Scenario: Token rotation on refresh
- **WHEN** el usuario refresh exitosamente
- **THEN** el sistema invalida el refresh_token usado y genera uno nuevo