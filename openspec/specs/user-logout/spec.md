## ADDED Requirements

### Requirement: User can logout
El sistema SHALL permitir que el usuario cierre sesión invalidando su refresh_token.

#### Scenario: Successful logout
- **WHEN** el usuario autenticado envía POST /api/v1/auth/logout con el refresh_token actual
- **THEN** el sistema elimina el refresh_token de la base de datos y el cliente debe descartar los tokens

#### Scenario: Logout with invalid token
- **WHEN** el usuario envía POST /api/v1/auth/logout con un token que no existe
- **THEN** el sistema devuelve error 404 Not Found o 200 OK sin efectos secundarios

### Requirement: Access token invalidation is not immediate
El sistema MUST reconocer que el access_token remains válido hasta su expiración natural (15 min).

#### Scenario: Token expiration after logout
- **WHEN** el usuario hace logout correctamente
- **THEN** el access_tokenremain válido hasta los 15 minutos deExpiration, pero el refresh_token está invalidado