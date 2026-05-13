## ADDED Requirements

### Requirement: Seed creates admin user with correct model fields
The seed script SHALL create an admin user using the actual Usuario model fields: nombre, email, password_hash, rol, telefono, activo, created_at, updated_at.

#### Scenario: Admin user created on first seed run
- **WHEN** the seed runs with an empty usuarios table
- **THEN** an admin user is created with email "admin@foodstore.com", rol "ADMIN", and a bcrypt-hashed password

#### Scenario: Seed is idempotent
- **WHEN** the seed runs a second time
- **THEN** no duplicate admin user is created

### Requirement: Seed uses real model imports
The seed script SHALL NOT import models that do not exist (Rol, UsuarioRol).

#### Scenario: Seed runs without ImportError
- **WHEN** the seed script is executed
- **THEN** all imports resolve successfully without conditional fallbacks to None

### Requirement: Seed documents available roles
The seed script SHALL document the 4 system roles (ADMIN, STOCK, PEDIDOS, CLIENT) even if they are stored as flat strings in the Usuario model.

#### Scenario: Roles are logged on seed execution
- **WHEN** the seed runs
- **THEN** the 4 roles are logged or printed to stdout for developer visibility
