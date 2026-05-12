## ADDED Requirements

### Requirement: Create MercadoPago payment preference
El sistema SHALL permitir al cliente iniciar un pago para un pedido en estado PENDIENTE creando una orden en MercadoPago via Orders API. El pago se registra en la tabla Pago con idempotency_key UUID único para evitar cobros duplicados (RN-PA02, RN-PA09).

#### Scenario: Successful payment creation
- **WHEN** un Cliente autenticado envía POST /api/v1/pagos/crear con un pedido_id válido en estado PENDIENTE del cual es propietario
- **THEN** el sistema genera un idempotency_key UUID, crea una orden en MercadoPago, persiste el registro Pago con status "pending", y retorna 201 con los datos de la preferencia (init_point, external_reference, idempotency_key)

#### Scenario: Order not in PENDIENTE state
- **WHEN** se intenta crear un pago para un pedido que no está en estado PENDIENTE
- **THEN** el sistema retorna 422 indicando que solo pedidos pendientes pueden iniciar pago

#### Scenario: Client not owner of order
- **WHEN** un Cliente intenta pagar un pedido que pertenece a otro usuario
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Duplicate idempotency key
- **WHEN** se recibe una solicitud de pago con un idempotency_key que ya existe en la BD
- **THEN** el sistema retorna 200 con el estado del pago existente (no crea uno nuevo)

### Requirement: Idempotency key must be unique per payment
El sistema SHALL generar y almacenar un idempotency_key UUID v4 único para cada intento de pago, garantizando que MercadoPago no procese el mismo cobro dos veces (RN-PA02).

#### Scenario: Idempotency key generated automatically
- **WHEN** se crea un nuevo pago via POST /api/v1/pagos/crear
- **THEN** el sistema genera automáticamente un UUID v4 como idempotency_key y lo envía a MercadoPago en el header X-Idempotency-Key

#### Scenario: Same key reused
- **WHEN** MercadoPago recibe una segunda solicitud con el mismo idempotency_key
- **THEN** MP devuelve el resultado del pago original sin procesar un nuevo cobro

### Requirement: Link payment to order via external_reference
El sistema SHALL vincular cada pago con su pedido usando el campo external_reference enviado a MercadoPago, que contiene el pedido_id y un identificador único corto (RN-PA09).

#### Scenario: External reference format
- **WHEN** se crea un pago para el pedido con id=42
- **THEN** el campo external_reference enviado a MP tiene el formato "pedido-42-{uuid_short}"
