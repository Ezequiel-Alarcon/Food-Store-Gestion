## MODIFIED Requirements

### Requirement: Create MercadoPago payment preference
El sistema SHALL permitir al cliente iniciar un pago para un pedido en estado PENDIENTE creando una orden en MercadoPago via Payments API. El pago se registra en la tabla Pago con idempotency_key UUID único para evitar cobros duplicados (RN-PA02, RN-PA09). El request a MP SHALL incluir datos completos del comprador (payer.email, payer.first_name, payer.last_name) para optimizar la validación antifraude y maximizar la tasa de aprobación.

#### Scenario: Successful payment creation
- **WHEN** un Cliente autenticado envía POST /api/v1/pagos/crear con un pedido_id válido en estado PENDIENTE del cual es propietario
- **THEN** el sistema genera un idempotency_key UUID, crea una orden en MercadoPago incluyendo payer.email, payer.first_name, y payer.last_name del usuario autenticado, persiste el registro Pago con status "pending", y retorna 201 con los datos del pago

#### Scenario: Order not in PENDIENTE state
- **WHEN** se intenta crear un pago para un pedido que no está en estado PENDIENTE
- **THEN** el sistema retorna 422 indicando que solo pedidos pendientes pueden iniciar pago

#### Scenario: Client not owner of order
- **WHEN** un Cliente intenta pagar un pedido que pertenece a otro usuario
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Duplicate idempotency key
- **WHEN** se recibe una solicitud de pago con un idempotency_key que ya existe en la BD
- **THEN** el sistema retorna 200 con el estado del pago existente (no crea uno nuevo)

## ADDED Requirements

### Requirement: Payer data must include email and name for fraud prevention
El sistema SHALL enviar los campos `payer.email`, `payer.first_name`, y `payer.last_name` al crear un pago en MercadoPago. Estos datos se obtienen del usuario autenticado (`current_user`). Los campos `payer.identification` (type y number) y `payer.phone` (area_code y number) SHALL enviarse si están disponibles en el perfil del usuario; si no, se omiten del request.

#### Scenario: Full payer data sent
- **WHEN** un Cliente con email, nombre, apellido, DNI y teléfono completos crea un pago
- **THEN** el request a MP incluye `payer.email`, `payer.first_name`, `payer.last_name`, `payer.identification.type="DNI"`, `payer.identification.number=<documento>`, `payer.phone.number=<telefono>`

#### Scenario: Partial payer data sent
- **WHEN** un Cliente crea un pago pero no tiene DNI ni teléfono registrados
- **THEN** el request a MP incluye solo `payer.email`, `payer.first_name`, y `payer.last_name`. Los campos `identification` y `phone` se omiten del request.

### Requirement: MercadoPago API errors mapped to appropriate HTTP status codes
El sistema SHALL clasificar los errores de la API de MercadoPago y retornar códigos HTTP apropiados en lugar de `422 ValidationError` genérico.

#### Scenario: MP returns 401 Unauthorized
- **WHEN** la API de MP devuelve error con status 401 (token inválido o expirado)
- **THEN** el sistema retorna 502 Bad Gateway con mensaje "Error de autenticación con el proveedor de pagos"

#### Scenario: MP returns 429 Too Many Requests
- **WHEN** la API de MP devuelve error con status 429 (rate limit)
- **THEN** el sistema retorna 503 Service Unavailable con mensaje "Proveedor de pagos momentáneamente no disponible. Reintente en unos segundos."

#### Scenario: Network timeout contacting MP
- **WHEN** la llamada a la API de MP excede el timeout de conexión
- **THEN** el sistema retorna 504 Gateway Timeout con mensaje "El proveedor de pagos no responde. Intente nuevamente."
