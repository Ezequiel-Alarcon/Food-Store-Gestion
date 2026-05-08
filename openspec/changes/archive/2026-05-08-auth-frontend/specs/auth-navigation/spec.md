## ADDED Requirements

### Requirement: Navigation shows login/register for guests
The Navigation component SHALL show "Ingresar" and "Registrarse" links when the user is not authenticated.

#### Scenario: Guest user sees auth links
- **WHEN** the user is not authenticated (isAuthenticated = false)
- **THEN** Navigation shows "Ingresar" and "Registrarse" links in the header

### Requirement: Navigation shows user menu for authenticated users
The Navigation component SHALL show the user's name and logout option when authenticated.

#### Scenario: Authenticated user sees user menu
- **WHEN** the user is authenticated with nombre "Juan"
- **AND** Navigation shows "Juan" dropdown with "Mi perfil" and "Cerrar sesión" options

### Requirement: Navigation shows menu by role - CLIENT
The Navigation SHALL show appropriate menu items for CLIENT role.

#### Scenario: CLIENT sees their menu
- **WHEN** user has role CLIENT
- **THEN** Navigation shows: Home, Productos, Mi Carrito, Mis Pedidos

### Requirement: Navigation shows menu by role - GESTOR_STOCK
The Navigation SHALL show appropriate menu items for GESTOR_STOCK role.

#### Scenario: GESTOR_STOCK sees their menu
- **WHEN** user has role GESTOR_STOCK
- **AND** Navigation shows: Home, Productos, Gestión de Stock

### Requirement: Navigation shows menu by role - GESTOR_PEDIDOS
The Navigation SHALL show appropriate menu items for GESTOR_PEDIDOS role.

#### Scenario: GESTOR_PEDIDOS sees their menu
- **WHEN** user has role GESTOR_PEDIDOS
- **AND** Navigation shows: Home, Productos, Gestión de Pedidos

### Requirement: Navigation shows menu by role - ADMIN
The Navigation SHALL show appropriate menu items for ADMIN role.

#### Scenario: ADMIN sees their menu
- **WHEN** user has role ADMIN
- **AND** Navigation shows: Home, Productos, Dashboard, Gestión de Usuarios

### Requirement: Logout clears session and redirects
The logout option SHALL clear the authStore and redirect to home/guest view.

#### Scenario: User clicks logout
- **WHEN** user clicks "Cerrar sesión"
- **AND** authStore is cleared
- **AND** user is redirected to home page
- **AND** Navigation now shows "Ingresar" and "Registrarse"