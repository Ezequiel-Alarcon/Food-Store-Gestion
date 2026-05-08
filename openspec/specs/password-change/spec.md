## ADDED Requirements

### Requirement: User can change their password
El sistema SHALL permitir que el usuario autenticado cambie su contraseña proporcionando la actual y la nueva.

#### Scenario: Successful password change
- **WHEN** el usuario envía PUT /api/v1/perfil/password con password_actual correcto y password_nuevo válido
- **THEN** el sistema actualiza el password y responde con éxito

#### Scenario: Wrong current password
- **WHEN** el usuario envía PUT /api/v1/perfil/password con password_actual incorrecto
- **THEN** el sistema devuelve error 401 Unauthorized con mensaje "Password actual incorrecta"

#### Scenario: New password too weak
- **WHEN** el usuario envía PUT /api/v1/perfil/password con password_nuevo con menos de 8 caracteres
- **THEN** el sistema devuelve error 422 con validación de Pydantic

### Requirement: Password change invalidates all refresh tokens
El sistema MUST invalidar todos los refresh tokens activos del usuario cuando cambia su password.

#### Scenario: Token invalidation after password change
- **WHEN** el usuario cambia su password exitosamente
- **THEN** el sistema elimina todos los refresh tokens asociados al usuario, forzando nuevo login