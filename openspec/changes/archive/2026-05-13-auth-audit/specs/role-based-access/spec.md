## ADDED Requirements

### Requirement: RolEnum is used for role validation
El sistema SHALL utilizar un enum Python `RolEnum` con los valores ADMIN, STOCK, PEDIDOS, CLIENT para validar roles en schemas Pydantic y en los parámetros de las dependencias de autorización. El string "GESTOR" no SHALL ser aceptado como rol válido.

#### Scenario: Valid role accepted
- **WHEN** un schema o endpoint recibe un rol "STOCK" o "PEDIDOS"
- **THEN** el sistema acepta el valor como rol válido

#### Scenario: Invalid role rejected
- **WHEN** un schema o endpoint recibe un rol "GESTOR" o cualquier string no definido en RolEnum
- **THEN** el sistema devuelve error 422 con validación de Pydantic

### Requirement: Gestor de Stock (STOCK) role access
Los endpoints de gestión de productos, stock e ingredientes SHALL ser accesibles para usuarios con rol STOCK.

#### Scenario: STOCK user accesses product endpoints
- **WHEN** el usuario con rol STOCK accede a endpoints CRUD de productos
- **THEN** el sistema permite el acceso

### Requirement: Gestor de Pedidos (PEDIDOS) role access
Los endpoints de gestión de pedidos SHALL ser accesibles para usuarios con rol PEDIDOS.

#### Scenario: PEDIDOS user accesses order management endpoints
- **WHEN** el usuario con rol PEDIDOS accede a endpoints de gestión de pedidos
- **THEN** el sistema permite el acceso
