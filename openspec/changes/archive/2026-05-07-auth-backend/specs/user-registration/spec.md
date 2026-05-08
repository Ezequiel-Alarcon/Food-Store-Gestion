## ADDED Requirements

### Requirement: User can register with email and password
El sistema SHALL permitir el registro de nuevos usuarios mediante email y password, asignando automáticamente el rol CLIENT al usuario registrado.

#### Scenario: Successful registration
- **WHEN** el usuario envía POST /api/v1/auth/register con email válido y password (mínimo 8 caracteres)
- **THEN** el sistema crea el usuario en la base de datos con rol CLIENT, devuelve access_token y refresh_token

#### Scenario: Registration with duplicate email
- **WHEN** el usuario intenta registrarse con un email que ya existe en el sistema
- **THEN** el sistema devuelve error 409 Conflict con mensaje "El email ya está registrado"

#### Scenario: Registration with invalid email format
- **WHEN** el usuario envía un email con formato inválido
- **THEN** el sistema devuelve error 422 con validación de Pydantic

#### Scenario: Registration with weak password
- **WHEN** el usuario envía password con menos de 8 caracteres
- **THEN** el sistema devuelve error 422 con mensaje "Password debe tener al menos 8 caracteres"

### Requirement: Password must be hashed before storage
El sistema MUST usar bcrypt con cost 12 para hashear passwords antes de almacenarlas en la base de datos.

#### Scenario: Password storage
- **WHEN** se crea un usuario
- **THEN** el password se almacena como hash bcrypt, nunca en texto plano