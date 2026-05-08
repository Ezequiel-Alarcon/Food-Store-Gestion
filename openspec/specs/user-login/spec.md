## ADDED Requirements

### Requirement: User can login with email and password
El sistema SHALL permitir el login de usuarios registrados mediante email y password, devolviendo access_token y refresh_token.

#### Scenario: Successful login
- **WHEN** el usuario envía POST /api/v1/auth/login con credenciales válidas
- **THEN** el sistema devuelve access_token (15 min) y refresh_token (7 días)

#### Scenario: Login with wrong password
- **WHEN** el usuario envía credentials correctas pero password incorrecto
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Credenciales inválidas"

#### Scenario: Login with non-existent email
- **WHEN** el usuario envía un email que no existe en el sistema
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Credenciales inválidas"

#### Scenario: Login rate limiting
- **WHEN** el usuario intenta hacer login más de 5 veces en 15 minutos desde la misma IP
- **THEN** el sistema devuelve error 429 Too Many Requests

### Requirement: JWT tokens must be signed with HS256
El sistema MUST usar algoritmo HS256 para firmar los tokens JWT con la clave configurada en SECRET_KEY.

#### Scenario: Token signature verification
- **WHEN** el cliente envía un request con access_token
- **THEN** el servidor verifica la firma HS256 del token antes de validar claims