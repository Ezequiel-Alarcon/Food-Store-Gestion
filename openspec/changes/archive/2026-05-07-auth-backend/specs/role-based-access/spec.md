## ADDED Requirements

### Requirement: Endpoints can be protected by roles
El sistema SHALL permitir proteger endpoints específicos para que solo ciertos roles puedan accederlos.

#### Scenario: Access with correct role
- **WHEN** el usuario con rol GESTOR accede a un endpoint protegido para GESTOR
- **THEN** el sistema permite el acceso y ejecuta la lógica del endpoint

#### Scenario: Access with incorrect role
- **WHEN** el usuario con rol CLIENT accede a un endpoint protegido solo para ADMIN
- **THEN** el sistema devuelve error 403 Forbidden con mensaje "No tienes permisos"

### Requirement: Roles hierarchy is enforced
El sistema MUST implementar jerarquía de roles: ADMIN > GESTOR > CLIENT.

#### Scenario: Admin access to all endpoints
- **WHEN** el usuario con rol ADMIN accede a cualquier endpoint
- **THEN** el sistema permite el acceso sin importar la protección del endpoint

#### Scenario: Gestor cannot access admin endpoints
- **WHEN** el usuario con rol GESTOR intenta acceder a un endpoint de administración
- **THEN** el sistema devuelve 403 Forbidden

### Requirement: Available roles are predefined
El sistema MUST incluir los roles predefinidos: ADMIN, GESTOR, CLIENT.

#### Scenario: Role assignment during registration
- **WHEN** un nuevo usuario se registra
- **THEN** el sistema asigna automáticamente el rol CLIENT

#### Scenario: Admin role can only be asignado por otro ADMIN
- **WHEN** un usuario no-ADMIN intenta asignar rol ADMIN a otro usuario
- **THEN** el sistema devuelve error 403 Forbidden