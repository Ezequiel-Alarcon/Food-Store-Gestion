## ADDED Requirements

### Requirement: New password must be different from current password
El sistema SHALL verificar que la nueva contraseña sea diferente de la contraseña actual antes de proceder con el cambio. Si son iguales, SHALL devolver error 400.

#### Scenario: New password same as current password
- **WHEN** el usuario envía PUT /api/v1/perfil/password con password_nuevo igual al password_actual
- **THEN** el sistema devuelve error 400 con mensaje "La nueva contraseña no puede ser igual a la actual"

#### Scenario: New password different from current password
- **WHEN** el usuario envía PUT /api/v1/perfil/password con password_nuevo diferente al password_actual y cumple requisitos de complejidad
- **THEN** el sistema procede con el cambio de contraseña
