## ADDED Requirements

### Requirement: Product delete returns confirmation message
El endpoint DELETE de productos SHALL devolver un mensaje de confirmación de eliminación exitosa.

#### Scenario: Product deleted with message
- **WHEN** se elimina un producto exitosamente
- **THEN** el sistema devuelve 200 con un mensaje indicando que el producto fue eliminado
