## ADDED Requirements

### Requirement: Delete ingredient works without error 500
El endpoint DELETE de ingredientes SHALL completar la operación sin error interno del servidor.

#### Scenario: Successful ingredient deletion
- **WHEN** se elimina un ingrediente existente
- **THEN** el sistema devuelve 200 con mensaje de confirmación
