## ADDED Requirements

### Requirement: Receive MercadoPago IPN webhook
El sistema SHALL exponer un endpoint público POST /api/v1/pagos/webhook que recibe notificaciones IPN de MercadoPago. El endpoint SHALL validar la autenticidad de la notificación mediante el header `x-signature` (ver `webhook-signature-validation`). Si la firma es válida, SHALL responder HTTP 200 inmediatamente y procesar la notificación de forma asíncrona usando BackgroundTasks. Si la firma es inválida, SHALL retornar 401 sin procesar la notificación (RN-PA03).

#### Scenario: Webhook receives valid payment notification
- **WHEN** MercadoPago envía POST /api/v1/pagos/webhook con topic=payment y resource_id, incluyendo header `x-signature` válido
- **THEN** el sistema retorna 200 OK inmediatamente y encola el procesamiento asíncrono del pago via BackgroundTasks

#### Scenario: Webhook with invalid signature
- **WHEN** el webhook incluye un header `x-signature` que no coincide con el HMAC calculado (estando `MP_WEBHOOK_SECRET` configurado)
- **THEN** el sistema retorna 401 Unauthorized y NO procesa la notificación

#### Scenario: Webhook with missing signature
- **WHEN** el webhook no incluye el header `x-signature` (estando `MP_WEBHOOK_SECRET` configurado)
- **THEN** el sistema retorna 401 Unauthorized

#### Scenario: Webhook with duplicate notification
- **WHEN** MercadoPago reenvía una notificación para un pago que ya fue procesado (mismo mp_payment_id y mismo status)
- **THEN** el sistema retorna 200 OK y NO realiza cambios (idempotencia)

### Requirement: Webhook processing is truly asynchronous
El sistema SHALL desacoplar la recepción de la notificación webhook de su procesamiento. La respuesta HTTP 200 debe enviarse ANTES de que comience el procesamiento (consulta a MP API, actualización de BD, confirmación de pedido). El procesamiento se ejecuta mediante `BackgroundTasks` de FastAPI en un thread separado.

#### Scenario: Response sent before processing begins
- **WHEN** el webhook recibe una notificación válida
- **THEN** el sistema retorna HTTP 200 en menos de 100ms, antes de consultar la API de MercadoPago o modificar la base de datos

#### Scenario: Processing failure does not affect response
- **WHEN** el BackgroundTask falla durante el procesamiento (ej: MP API timeout, error de BD)
- **THEN** el HTTP 200 ya fue enviado. El error se registra en logs. MercadoPago reenviará la notificación según su política de retry (15 min, hasta 3 intentos).

### Requirement: Verify payment status against MercadoPago API
El sistema SHALL consultar siempre el estado real del pago a MercadoPago API (GET /v1/payments/{id}) al recibir una notificación IPN. Nunca se debe confiar exclusivamente en los datos del webhook (RN-PA04).

#### Scenario: Payment approved according to MP API
- **WHEN** el webhook notifica un pago y la consulta a MP API devuelve status="approved"
- **THEN** el sistema actualiza Pago.status="approved", avanza el Pedido a CONFIRMADO, decrementa stock, y registra en historial con actor=SISTEMA

#### Scenario: Payment rejected according to MP API
- **WHEN** el webhook notifica un pago y la consulta a MP API devuelve status="rejected"
- **THEN** el sistema actualiza Pago.status="rejected" y Pago.status_detail con el motivo de rechazo. El Pedido permanece en PENDIENTE (RN-PA06).

#### Scenario: Payment pending or in_process according to MP API
- **WHEN** el webhook notifica un pago y la consulta a MP API devuelve status="pending" o "in_process"
- **THEN** el sistema actualiza Pago.status al valor correspondiente. El Pedido permanece en PENDIENTE (RN-PA07).

### Requirement: Automatic order confirmation on payment approved
El sistema SHALL transicionar automáticamente el pedido de PENDIENTE a CONFIRMADO cuando el pago asociado es aprobado por MercadoPago. Esta transición es ejecutada por el SISTEMA, nunca por un usuario manualmente (RN-FS02, RN-PA05).

#### Scenario: Atomic confirmation with stock decrement
- **WHEN** un pago es aprobado, el sistema ejecuta en una única transacción UoW: actualizar Pago, cambiar Pedido.estado_codigo a CONFIRMADO, insertar HistorialEstadoPedido con actor=SISTEMA, y decrementar stock de cada producto del pedido
- **THEN** si cualquier paso falla, toda la transacción hace rollback y el pedido permanece en PENDIENTE

#### Scenario: Confirmation with insufficient stock
- **WHEN** un pago es aprobado pero algún producto no tiene stock suficiente
- **THEN** la transacción hace rollback completo y el pedido permanece en PENDIENTE

#### Scenario: Stock decrement is per-item
- **WHEN** un pedido tiene 3 líneas (2 unidades de Producto A, 1 de Producto B, 5 de Producto C)
- **THEN** el stock de A se decrementa en 2, B en 1, C en 5

### Requirement: Payment status transitions are recorded
El sistema SHALL registrar cada cambio de estado del Pago (status y status_detail) con timestamp de actualización.

#### Scenario: Payment status history
- **WHEN** un pago pasa de "pending" a "approved"
- **THEN** el campo actualizado_en refleja el momento exacto de la transición y status_detail se actualiza con el detalle provisto por MP
