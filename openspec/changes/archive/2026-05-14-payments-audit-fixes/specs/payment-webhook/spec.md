## MODIFIED Requirements

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
