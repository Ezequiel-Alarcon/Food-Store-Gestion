## ADDED Requirements

### Requirement: get_current_user uses HTTPBearer for token extraction
La dependencia get_current_user SHALL usar HTTPBearer (no OAuth2PasswordBearer) para extraer el token JWT del header Authorization. El token extraído se obtiene del atributo `credentials` del objeto HTTPAuthorizationCredentials.

#### Scenario: Token extraction via HTTPBearer
- **WHEN** un request incluye Authorization: Bearer <token>
- **THEN** get_current_user extrae el token correctamente del header

### Requirement: get_current_user rejects non-access tokens
La dependencia get_current_user SHALL verificar que el payload del JWT contenga el claim "type" con valor "access". Tokens sin este claim o con un valor diferente (ej: "refresh") SHALL ser rechazados con error de autenticación.

#### Scenario: Access token accepted
- **WHEN** un request incluye un JWT cuyo payload contiene "type": "access"
- **THEN** get_current_user resuelve el usuario correctamente

#### Scenario: Refresh token rejected as access token
- **WHEN** un request incluye un refresh_token en el header Authorization (token con payload sin "type": "access")
- **THEN** get_current_user rechaza el request con error 401 Unauthorized

#### Scenario: Token without type claim rejected
- **WHEN** un request incluye un JWT cuyo payload no contiene el claim "type"
- **THEN** get_current_user rechaza el request con error 401 Unauthorized
