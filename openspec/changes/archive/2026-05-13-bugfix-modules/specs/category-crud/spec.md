## ADDED Requirements

### Requirement: CTE queries use text() wrapper
Las queries SQL textuales (CTE recursivas) en el repositorio de categorías MUST usar el wrapper `text()` de SQLAlchemy para cumplir con SQLAlchemy 2.0+.

#### Scenario: Delete category with descendants
- **WHEN** se elimina una categoría con subcategorías
- **THEN** la query CTE se ejecuta sin error 500
