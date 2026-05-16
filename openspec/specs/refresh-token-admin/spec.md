## ADDED Requirements

### Requirement: Admin can list active refresh tokens for a user
El sistema SHALL permitir a un administrador listar todos los refresh tokens activos (no revocados y no expirados) de un usuario específico.

#### Scenario: Successful token list
- **WHEN** un admin envía GET /api/v1/refreshtokens/user/{user_id} con token válido y rol admin
- **THEN** el sistema devuelve una lista de refresh tokens activos con id, user_id, expires_at, created_at, y revocado

#### Scenario: List tokens for non-existent user
- **WHEN** un admin envía GET /api/v1/refreshtokens/user/{user_id} con user_id que no existe
- **THEN** el sistema devuelve error 404 Not Found

#### Scenario: Non-admin attempts to list tokens
- **WHEN** un usuario sin rol admin envía GET /api/v1/refreshtokens/user/{user_id}
- **THEN** el sistema devuelve error 403 Forbidden

### Requirement: Admin can revoke a specific refresh token
El sistema SHALL permitir a un administrador revocar un refresh token específico por su ID.

#### Scenario: Successful token revocation
- **WHEN** un admin envía POST /api/v1/refreshtokens/revoke/{token_id} con token válido y rol admin
- **THEN** el sistema marca el token como revocado y devuelve confirmación con id y user_id del token revocado

#### Scenario: Revoke non-existent token
- **WHEN** un admin envía POST /api/v1/refreshtokens/revoke/{token_id} con token_id que no existe
- **THEN** el sistema devuelve error 404 Not Found

#### Scenario: Revoke already revoked token
- **WHEN** un admin envía POST /api/v1/refreshtokens/revoke/{token_id} con token ya revocado
- **THEN** el sistema devuelve error 400 Bad Request con mensaje "Token ya revocado"

### Requirement: Admin can revoke all refresh tokens for a user
El sistema SHALL permitir a un administrador revocar TODOS los refresh tokens activos de un usuario específico (forced logout).

#### Scenario: Successful bulk revocation
- **WHEN** un admin envía DELETE /api/v1/refreshtokens/user/{user_id}/all con token válido y rol admin
- **THEN** el sistema revoca todos los tokens activos del usuario y devuelve la cantidad de tokens revocados

#### Scenario: Bulk revoke for user with no active tokens
- **WHEN** un admin envía DELETE /api/v1/refreshtokens/user/{user_id}/all y el usuario no tiene tokens activos
- **THEN** el sistema devuelve 200 con cantidad 0

### Requirement: Module is registered in FastAPI app
El módulo refreshtokens SHALL estar registrado en la aplicación FastAPI con prefijo `/api/v1/refreshtokens` y tag `refreshtokens`.

#### Scenario: Module registration
- **WHEN** la aplicación FastAPI inicia
- **THEN** el router de refreshtokens está disponible bajo `/api/v1/refreshtokens`

### Requirement: RefreshTokenService uses Unit of Work
El servicio de refresh tokens SHALL usar el patrón Unit of Work para todas las operaciones de escritura.

#### Scenario: Token creation within UoW
- **WHEN** se crea un nuevo refresh token a través del service
- **THEN** la operación se ejecuta dentro de un contexto `with uow:` y hace commit automático

#### Scenario: Token revocation rollback on error
- **WHEN** ocurre un error durante la revocación de un token
- **THEN** la transacción se revierte automáticamente y el token no se marca como revocado
