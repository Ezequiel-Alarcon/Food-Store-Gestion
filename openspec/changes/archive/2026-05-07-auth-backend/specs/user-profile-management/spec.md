## ADDED Requirements

### Requirement: User can view their own profile
El sistema SHALL permitir que el usuario autenticado vea su propio perfil.

#### Scenario: Successful profile view
- **WHEN** el usuario envía GET /api/v1/perfil
- **THEN** el sistema devuelve los datos del perfil (email, nombre, rol, fecha de creación)

#### Scenario: Unauthenticated profile access
- **WHEN** un usuario no autenticado intenta acceder a GET /api/v1/perfil
- **THEN** el sistema devuelve error 401 Unauthorized

### Requirement: User can update their own profile
El sistema SHALL permitir que el usuario autenticado actualice su nombre y otros datos (excepto email y rol).

#### Scenario: Successful profile update
- **WHEN** el usuario envía PUT /api/v1/perfil con datos válidos
- **THEN** el sistema actualiza los campos y devuelve el perfil actualizado

#### Scenario: Update attempt on protected fields
- **WHEN** el usuario intenta actualizar su email o rol
- **THEN** el sistema ignora esos campos o devuelve error 422

### Requirement: Users can only access their own profile
El sistema MUST prevenir que un usuario acceda o modifique el perfil de otro usuario.

#### Scenario: Cross-user profile access prevention
- **WHEN** el usuario autenticado intenta acceder a otro perfil mediante ID
- **THEN** el sistema devuelve error 403 Forbidden o404 Not Found