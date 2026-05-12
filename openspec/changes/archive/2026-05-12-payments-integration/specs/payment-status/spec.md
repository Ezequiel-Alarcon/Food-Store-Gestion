## ADDED Requirements

### Requirement: Query payment status for an order
El sistema SHALL permitir consultar el estado del pago asociado a un pedido via GET /api/v1/pagos/{pedido_id}. Solo el propietario del pedido o un administrador pueden acceder.

#### Scenario: Client queries own order payment
- **WHEN** un Cliente autenticado envía GET /api/v1/pagos/{pedido_id} sobre un pedido propio
- **THEN** el sistema retorna 200 con: status del pago (pending|approved|rejected|in_process), mp_payment_id si existe, transaction_amount, payment_method_id, status_detail, fechas de creación y última actualización

#### Scenario: Client queries another user's order payment
- **WHEN** un Cliente intenta consultar el pago de un pedido que no le pertenece
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Admin queries any order payment
- **WHEN** un Admin envía GET /api/v1/pagos/{pedido_id} sobre cualquier pedido
- **THEN** el sistema retorna 200 con los datos completos del pago

#### Scenario: Order has no payment yet
- **WHEN** se consulta un pedido que no tiene ningún pago registrado
- **THEN** el sistema retorna 404 con mensaje indicando que no hay pagos para ese pedido

### Requirement: Payment response includes MercadoPago status details
El sistema SHALL incluir en la respuesta de consulta el campo status_detail con el detalle textual provisto por MercadoPago (ej: "accredited", "cc_rejected_insufficient_amount", "pending_contingency").

#### Scenario: Payment with detailed rejection reason
- **WHEN** un pago fue rechazado por fondos insuficientes
- **THEN** la respuesta incluye status="rejected" y status_detail="cc_rejected_insufficient_amount" para que el frontend muestre el motivo al cliente
