## ADDED Requirements

### Requirement: Retry rejected payment
El sistema SHALL permitir al cliente reintentar un pago cuando el intento anterior fue rechazado. El reintento genera un nuevo idempotency_key y una nueva orden en MercadoPago. El pedido permanece en PENDIENTE (RN-PA08).

#### Scenario: Successful payment retry
- **WHEN** un Cliente envía POST /api/v1/pagos/{pedido_id}/reintentar sobre un pedido propio en PENDIENTE cuyo último pago fue rechazado
- **THEN** el sistema genera un nuevo idempotency_key, crea una nueva orden en MercadoPago, persiste un nuevo registro Pago (relación 1:N), y retorna 201 con los datos de la nueva preferencia

#### Scenario: Retry when last payment is still pending
- **WHEN** un Cliente intenta reintentar un pago cuyo último intento está en estado "pending" o "in_process"
- **THEN** el sistema retorna 422 indicando que el pago aún está en proceso y no se puede reintentar

#### Scenario: Retry when last payment is approved
- **WHEN** un Cliente intenta reintentar un pago que ya fue aprobado
- **THEN** el sistema retorna 422 indicando que el pago ya fue aprobado

#### Scenario: Multiple payment attempts preserved
- **WHEN** un pedido ha tenido 3 intentos de pago (2 rechazados, 1 aprobado)
- **THEN** la tabla Pago contiene 3 registros, todos vinculados al mismo pedido_id, cada uno con su propio idempotency_key y mp_payment_id

#### Scenario: Retry on non-owned order
- **WHEN** un Cliente intenta reintentar el pago de un pedido que no le pertenece
- **THEN** el sistema retorna 403 Forbidden

### Requirement: Automatic cleanup of abandoned payments not required
El sistema NO requiere limpiar o cancelar pagos pendientes antiguos. MercadoPago los expira automáticamente. Solo se registra el nuevo intento.
