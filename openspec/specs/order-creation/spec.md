## ADDED Requirements

### Requirement: Create order atomically with snapshots
El sistema SHALL crear un pedido de forma completamente atómica usando Unit of Work. Si cualquier parte falla (validación de stock, snapshot, persistencia), no se persiste ningún registro.

#### Scenario: Successful order creation
- **WHEN** un Cliente autenticado envía POST /api/v1/pedidos con una lista de ítems válidos y una dirección propia
- **THEN** el sistema retorna 201 Created con el pedido en estado PENDIENTE, incluyendo los ítems con precio_unitario snapshot y el snapshot de dirección

#### Scenario: Order with insufficient stock
- **WHEN** algún ítem del pedido tiene una cantidad mayor al stock disponible del producto
- **THEN** el sistema retorna 422 con detalle del producto y stock disponible; no se crea ningún registro en base de datos

#### Scenario: Stock lock during concurrent requests
- **WHEN** dos clientes intentan crear pedidos con el último ítem del mismo producto simultáneamente
- **THEN** solo uno obtiene 201; el otro obtiene 422 por stock insuficiente; el stock no queda negativo

#### Scenario: Unauthenticated user attempts to create order
- **WHEN** se envía POST /api/v1/pedidos sin token JWT válido
- **THEN** el sistema retorna 401 Unauthorized

### Requirement: Price snapshot per item
El sistema SHALL almacenar el precio actual del producto en el campo `precio_unitario` de cada `DetallePedido` en el momento de la creación. Cambios posteriores al precio del producto no afectan pedidos existentes.

#### Scenario: Price changes after order creation
- **WHEN** el precio de un producto es modificado después de que un pedido fue creado
- **THEN** el pedido mantiene el precio original en precio_unitario (snapshot inmutable)

#### Scenario: Order total calculated from snapshots
- **WHEN** se consulta el total de un pedido
- **THEN** el total refleja la suma de (cantidad × precio_unitario) de cada ítem más costo_envio

### Requirement: Address snapshot in order
El sistema SHALL copiar los campos de la dirección de entrega directamente en el pedido (calle, ciudad, provincia, código postal, referencia) al momento de la creación.

#### Scenario: Address deleted after order creation
- **WHEN** el cliente elimina una dirección que fue usada en un pedido existente
- **THEN** el pedido conserva el snapshot de dirección original; la eliminación no afecta el pedido

#### Scenario: Order created with address from another user
- **WHEN** un Cliente intenta crear un pedido con el ID de una dirección que no le pertenece
- **THEN** el sistema retorna 403 Forbidden; no se crea el pedido

### Requirement: Initial state audit entry
El sistema SHALL registrar una entrada en HistorialEstadoPedido al crear el pedido, con estado_anterior NULL y estado_nuevo PENDIENTE, actor_tipo USUARIO.

#### Scenario: History created on new order
- **WHEN** un pedido es creado exitosamente
- **THEN** existe exactamente un registro en HistorialEstadoPedido con estado_nuevo=PENDIENTE y estado_anterior=NULL

### Requirement: Ingredient exclusions stored per item
El sistema SHALL almacenar las exclusiones de ingredientes como un array de IDs (INTEGER[]) en el campo `exclusiones` de cada DetallePedido.

#### Scenario: Order item with ingredient exclusions
- **WHEN** un cliente crea un pedido excluyendo ingredientes de un ítem
- **THEN** el DetallePedido almacena el array de IDs de ingredientes excluidos

#### Scenario: Order item without exclusions
- **WHEN** un cliente crea un pedido sin exclusiones para un ítem
- **THEN** el campo exclusiones es un array vacío (no NULL)

### Requirement: Get order detail by ID
El sistema SHALL retornar el detalle completo de un pedido (con ítems y estado actual) vía GET /api/v1/pedidos/{id}, respetando RBAC.

#### Scenario: Client views own order
- **WHEN** un Cliente autenticado solicita GET /api/v1/pedidos/{id} de un pedido propio
- **THEN** el sistema retorna 200 con el pedido completo incluyendo ítems

#### Scenario: Client attempts to view another user's order
- **WHEN** un Cliente autenticado solicita GET /api/v1/pedidos/{id} de un pedido de otro usuario
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Gestor de Pedidos views any order
- **WHEN** un usuario con rol PEDIDOS solicita GET /api/v1/pedidos/{id}
- **THEN** el sistema retorna 200 con el pedido completo independientemente del propietario
