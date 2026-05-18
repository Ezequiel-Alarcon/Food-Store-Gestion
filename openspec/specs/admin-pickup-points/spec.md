## Requirements

### Requirement: Admin can view list of branches
El sistema SHALL mostrar una tabla de sucursales en `/admin/sucursales` accesible solo para ADMIN, con el nombre de la sucursal, su dirección asociada, y estado (activa/inactiva).

#### Scenario: Admin views branch list
- **WHEN** un ADMIN navega a `/admin/sucursales`
- **THEN** el sistema muestra una tabla con todas las sucursales y sus direcciones asociadas
- **AND** cada fila muestra nombre, dirección formateada, y badge de estado

#### Scenario: Non-admin cannot access branch management
- **WHEN** un usuario sin rol ADMIN intenta acceder a `/admin/sucursales`
- **THEN** el sistema redirige a `/` o muestra 403

### Requirement: Admin can create a branch with address
El sistema SHALL permitir a ADMIN crear una nueva sucursal con su dirección en un solo formulario.

#### Scenario: Admin creates branch with address
- **WHEN** un ADMIN completa el formulario con nombre de sucursal y campos de dirección (calle, número, ciudad, provincia, país)
- **THEN** el sistema crea la sucursal via `POST /branches/` y luego la dirección via `POST /branches/{id}/address`
- **AND** muestra toast de éxito y refresca la tabla

#### Scenario: Admin creates branch with validation errors
- **WHEN** un ADMIN envía el formulario con campos inválidos (nombre vacío, calle vacía, etc.)
- **THEN** el sistema muestra errores de validación en el formulario

### Requirement: Admin can edit a branch name and address
El sistema SHALL permitir a ADMIN editar el nombre de una sucursal y su dirección asociada.

#### Scenario: Admin edits branch
- **WHEN** un ADMIN abre el modal de edición de una sucursal y modifica el nombre o dirección
- **THEN** el sistema actualiza via `PATCH /branches/{id}` y `PATCH /branches/{id}/address`
- **AND** muestra toast de éxito y refresca la tabla

### Requirement: Admin can delete (soft-delete) a branch
El sistema SHALL permitir a ADMIN desactivar una sucursal (soft-delete).

#### Scenario: Admin deletes branch
- **WHEN** un ADMIN confirma la eliminación de una sucursal
- **THEN** el sistema actualiza `activa: false` via `PATCH /branches/{id}`
- **AND** la sucursal deja de aparecer en la tabla (o se muestra como inactiva)

### Requirement: Branch management navigation
El sistema SHALL mostrar la opción "Sucursales" en el menú de navegación para ADMIN.

#### Scenario: Admin sees branch management in nav
- **WHEN** un ADMIN inicia sesión
- **THEN** el menú de navegación incluye "Sucursales" con link a `/admin/sucursales`
