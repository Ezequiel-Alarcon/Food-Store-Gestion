## ADDED Requirements

### Requirement: Admin can list all users
El sistema SHALL permitir a ADMIN y GESTOR listar todos los usuarios con paginación.

#### Scenario: List users as admin
- **WHEN** ADMIN envía GET /api/v1/usuarios/?offset=0&limit=10
- **THEN** el sistema devuelve array de usuarios con id, email, nombre, rol, telefono, activo, created_at

#### Scenario: List users excludes inactive by default
- **WHEN** GESTOR envía GET /api/v1/usuarios/ (sin include_inactive)
- **THEN** el sistema devuelve solo usuarios con activo=true

#### Scenario: List users includes inactive
- **WHEN** ADMIN envía GET /api/v1/usuarios/?include_inactive=true
- **THEN** el sistema devuelve todos los usuarios incluyendo inactivos

### Requirement: Admin can view a specific user
El sistema SHALL permitir a ADMIN y GESTOR obtener un usuario por ID.

#### Scenario: Get existing user
- **WHEN** ADMIN envía GET /api/v1/usuarios/1
- **THEN** el sistema devuelve datos completos del usuario

#### Scenario: Get non-existent user
- **WHEN** ADMIN envía GET /api/v1/usuarios/99999
- **THEN** el sistema devuelve 404 Not Found con mensaje "Usuario no encontrado"

### Requirement: Admin can update user data
El sistema SHALL permitir a ADMIN actualizar datos de un usuario (nombre, rol, telefono, activo).

#### Scenario: Update user successfully
- **WHEN** ADMIN envía PUT /api/v1/usuarios/1?nombre=Nuevo+Nombre
- **THEN** el sistema actualiza el campo y devuelve el usuario actualizado

#### Scenario: Update user with new role
- **WHEN** ADMIN envía PUT /api/v1/usuarios/1?rol=GESTOR
- **THEN** el sistema actualiza el rol del usuario

#### Scenario: Update user as non-admin
- **WHEN** GESTOR envía PUT /api/v1/usuarios/1?nombre=Test
- **THEN** el sistema devuelve 403 Forbidden

#### Scenario: Update non-existent user
- **WHEN** ADMIN envía PUT /api/v1/usuarios/99999?nombre=Test
- **THEN** el sistema devuelve 404 Not Found

### Requirement: Admin can deactivate a user
El sistema SHALL permitir a ADMIN desactivar un usuario (soft delete).

#### Scenario: Deactivate user successfully
- **WHEN** ADMIN envía DELETE /api/v1/usuarios/1
- **THEN** el sistema marca usuario como activo=false y devuelve mensaje "Usuario desactivado correctamente"

#### Scenario: Deactivate user as non-admin
- **WHEN** GESTOR envía DELETE /api/v1/usuarios/1
- **THEN** el sistema devuelve 403 Forbidden

#### Scenario: Deactivate non-existent user
- **WHEN** ADMIN envía DELETE /api/v1/usuarios/99999
- **THEN** el sistema devuelve 404 Not Found