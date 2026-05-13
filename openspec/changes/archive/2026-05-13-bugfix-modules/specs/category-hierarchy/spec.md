## ADDED Requirements

### Requirement: get_subcategorias uses text() wrapper
La query CTE recursiva para obtener subcategorías MUST usar `text()` wrapper.

#### Scenario: Get subcategories without error
- **WHEN** se solicitan subcategorías de una categoría
- **THEN** la respuesta es 200 con la lista de subcategorías
