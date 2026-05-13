## ADDED Requirements

### Requirement: RegisterRequest includes apellido field
El schema RegisterRequest MUST incluir un campo "apellido" de tipo string con un mínimo de 2 caracteres y un máximo de 80 caracteres.

#### Scenario: Registration with missing apellido
- **WHEN** el usuario envía POST /api/v1/auth/register sin el campo apellido
- **THEN** el sistema devuelve error 422 con validación de Pydantic

#### Scenario: Registration with too short apellido
- **WHEN** el usuario envía apellido con menos de 2 caracteres
- **THEN** el sistema devuelve error 422 con mensaje de validación de longitud mínima

### Requirement: Password must contain uppercase and number
El password suministrado en RegisterRequest MUST contener al menos 1 letra mayúscula y al menos 1 número, además del mínimo de 8 caracteres.

#### Scenario: Registration with password missing uppercase
- **WHEN** el usuario envía un password de 8+ caracteres pero sin letras mayúsculas
- **THEN** el sistema devuelve error 422 con mensaje indicando que se requiere al menos 1 mayúscula

#### Scenario: Registration with password missing number
- **WHEN** el usuario envía un password de 8+ caracteres pero sin números
- **THEN** el sistema devuelve error 422 con mensaje indicando que se requiere al menos 1 número

#### Scenario: Registration with valid complex password
- **WHEN** el usuario envía un password con 8+ caracteres, al menos 1 mayúscula, y al menos 1 número
- **THEN** la validación de password es exitosa y continúa el flujo de registro

### Requirement: Whitespace in password is properly handled
El sistema SHALL aplicar strip() al password recibido en RegisterRequest antes de validar su complejidad y antes de hashearlo.

#### Scenario: Password with leading/trailing whitespace
- **WHEN** el usuario envía un password con espacios al inicio o al final
- **THEN** el sistema elimina los espacios antes de validar y hashear
