## ADDED Requirements

### Requirement: Seed de Roles
El script debe insertar los 4 roles del sistema RBAC.

#### Scenario: Ejecutar seed de roles
- **WHEN** python -m app.db.seed se ejecuta
- **THEN** crea registros: ADMIN, STOCK, PEDIDOS, CLIENT en tabla Rol

#### Scenario: Seed ya ejecutado
- **WHEN** seed se ejecuta nuevamente
- **THEN** no duplica registros (upsert o skip si existen)

### Requirement: Seed de EstadosPedido
El script debe insertar los 6 estados de la máquina de estados del pedido.

#### Scenario: Ejecutar seed de estados
- **WHEN** seed crea estados de pedido
- **THEN** crea: PENDIENTE (orden 1), CONFIRMADO (2), EN_PREP (3), EN_CAMINO (4), ENTREGADO (5), CANCELADO (6)
- **AND** es_terminal=true para ENTREGADO y CANCELADO, false para los demás

### Requirement: Seed de FormaPago
El script debe insertar las 3 formas de pago del sistema.

#### Scenario: Ejecutar seed de formas de pago
- **WHEN** seed crea formas de pago
- **THEN** crea: MERCADOPAGO, EFECTIVO, TRANSFERENCIA con habilitado=true

### Requirement: Seed de usuario admin
El script debe crear el usuario administrador inicial.

#### Scenario: Crear usuario admin
- **WHEN** seed ejecuta
- **THEN** crea usuario admin@foodstore.com con password hasheada (bcrypt cost 12)
- **AND** asigna rol ADMIN al usuario
- **AND** credenciales: Admin1234!

### Requirement: Orden de ejecución
El seed debe ejecutarse DESPUÉS de las migraciones.

#### Scenario: Seed sin migraciones
- **WHEN** seed se ejecuta antes de alembic upgrade head
- **THEN** falla por tablas inexistentes