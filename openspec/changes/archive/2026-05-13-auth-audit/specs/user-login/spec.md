## ADDED Requirements

### Requirement: Login returns generic message for all failure cases
El sistema SHALL devolver el mismo mensaje genérico "Credenciales inválidas" para todos los casos de fallo de autenticación (email inexistente, password incorrecto, usuario inactivo), según RN-AU08.

#### Scenario: Login with inactive user
- **WHEN** el usuario envía credenciales correctas pero su cuenta está desactivada (activo=false)
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Credenciales inválidas"

### Requirement: Access token JWT payload includes type claim
El access token JWT payload MUST incluir un claim "type" con valor "access" para que get_current_user pueda distinguir access tokens de refresh tokens.

#### Scenario: Access token contains type claim
- **WHEN** el sistema genera un access_token mediante create_access_token()
- **THEN** el payload JWT incluye "type": "access" además de sub, exp, y rol

#### Scenario: Non-access token rejected by get_current_user
- **WHEN** un request incluye un token JWT cuyo payload NO contiene "type": "access"
- **THEN** get_current_user rechaza el request con error de autenticación
