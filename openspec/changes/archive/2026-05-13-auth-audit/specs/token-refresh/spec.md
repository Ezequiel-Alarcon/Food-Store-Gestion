## ADDED Requirements

### Requirement: Disabled user cannot refresh tokens
El sistema SHALL rechazar el refresh de tokens si la cuenta del usuario está desactivada (activo=false), verificando el campo activo del Usuario ANTES de revocar el refresh_token y ANTES de emitir nuevos tokens.

#### Scenario: Refresh token rejected for disabled user
- **WHEN** el usuario envía POST /api/v1/auth/refresh con refresh_token válido pero su cuenta está desactivada
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Credenciales inválidas" y NO revoca el refresh_token

### Requirement: Token expiry uses timezone-aware datetime comparison
El sistema SHALL usar datetime timezone-aware (UTC) para comparar la expiración de refresh tokens. La comparación `expires_at > now` MUST usar `datetime.now(timezone.utc)` en lugar de `datetime.utcnow()`.

#### Scenario: Expiry check with timezone-aware datetime
- **WHEN** el sistema verifica si un refresh_token ha expirado
- **THEN** la comparación se realiza con `datetime.now(timezone.utc)` para evitar discrepancias naive-vs-aware con PostgreSQL
