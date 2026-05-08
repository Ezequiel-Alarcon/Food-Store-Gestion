## ADDED Requirements

### Requirement: Hierarchical Tree Listing
The system SHALL provide endpoints to retrieve categories in hierarchical tree format using PostgreSQL CTE recursive queries.

#### Scenario: Get full category tree
- **WHEN** any user sends GET `/api/v1/categorias/arbol`
- **THEN** system returns 200 with nested tree structure
- **AND** root categories (padre_id=null) are at top level
- **AND** each category includes `hijos: []` array with nested children
- **AND** only active categories are included

#### Scenario: Tree structure example
```
- Comidas (root)
  - Italiana
    - Pizzas
    - Pastas
  - Japonesa
    - Sushi
- Bebidas (root)
  - Sin Alcohol
  - Con Alcohol
```

#### Scenario: Empty tree (no categories)
- **WHEN** user sends GET `/api/v1/categorias/arbol`
- **AND** no categories exist
- **THEN** system returns 200 with empty array `[]`

#### Scenario: Tree respects order field
- **WHEN** categories have explicit `orden` values
- **THEN** siblings are sorted by `orden` ascending, then alphabetically by `nombre`
- **AND** descendants maintain their own ordering within parent

---

### Requirement: Get Category Descendants
The system SHALL provide endpoint to get all descendants of a category using CTE.

#### Scenario: Get direct children only
- **WHEN** authenticated user sends GET `/api/v1/categorias/1/subcategorias`
- **AND** depth parameter is not provided or depth=1
- **THEN** system returns direct children only (level 1)
- **AND** returns 200 with list of child categories

#### Scenario: Get descendants with depth
- **WHEN** authenticated user sends GET `/api/v1/categorias/1/subcategorias?profundidad=3`
- **THEN** system returns all descendants up to 3 levels deep
- **AND** includes grandchildren, great-grandchildren, etc.

#### Scenario: Get descendants for leaf category
- **WHEN** user sends GET `/api/v1/categorias/99/subcategorias`
- **AND** category has no children
- **THEN** system returns 200 with empty array

#### Scenario: Get descendants for non-existent category
- **WHEN** user sends GET `/api/v1/categorias/9999/subcategorias`
- **THEN** system returns 404 Not Found

---

### Requirement: Cycle Prevention
The system SHALL prevent creating cycles in the category hierarchy. A category cannot be its own ancestor.

#### Scenario: Cannot set category as its own parent
- **WHEN** authenticated ADMIN sends PUT `/api/v1/categorias/1` with `padre_id: 1`
- **THEN** system returns 400 Bad Request
- **AND** error message indicates cycle detected

#### Scenario: Cannot set category as descendant's parent
- **WHEN** category tree exists: Comidas → Italiana → Pizzas
- **AND** authenticated ADMIN sends PUT `/api/v1/categorias/1` (Comidas) with `padre_id: 3` (Pizzas)
- **THEN** system returns 400 Bad Request
- **AND** error message indicates cycle detected ("Pizzas is a descendant of Comidas")

#### Scenario: Cannot create new category with cycle
- **WHEN** authenticated ADMIN sends POST `/api/v1/categorias/` with `padre_id: 3`
- **AND** setting padre_id=3 would create a cycle
- **THEN** system returns 400 Bad Request

#### Scenario: Can move category to different branch
- **WHEN** category tree exists: Comidas → Italiana → Pizzas
- **AND** authenticated ADMIN sends PUT `/api/v1/categorias/3` (Pizzas) with `padre_id: null` (make root)
- **THEN** system updates successfully
- **AND** returns 200

#### Scenario: Can move category under different parent
- **WHEN** category tree exists: Comidas → Italiana, Bebidas
- **AND** authenticated ADMIN sends PUT `/api/v1/categorias/2` (Italiana) with `padre_id: 3` (Bebidas)
- **AND** this does not create a cycle
- **THEN** system updates successfully
- **AND** Italiana is now child of Bebidas

---

### Requirement: Public Category Listing
The system SHALL provide a public endpoint for category tree accessible without authentication.

#### Scenario: Public tree access
- **WHEN** unauthenticated user sends GET `/api/v1/categorias/publico/arbol`
- **THEN** system returns 200 with nested tree structure
- **AND** only active categories are included
- **AND** rate limiting applies (slowapi)

#### Scenario: Public tree for frontend menu
- **WHEN** frontend requests GET `/api/v1/categorias/publico/arbol`
- **THEN** response is optimized for menu rendering
- **AND** includes `id`, `nombre`, `slug` for each category
- **AND** includes `hijos` for nested navigation
