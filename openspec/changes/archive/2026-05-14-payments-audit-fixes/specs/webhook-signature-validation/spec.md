## ADDED Requirements

### Requirement: Validate webhook notification authenticity via HMAC SHA256 signature
El sistema SHALL validar que las notificaciones webhook recibidas en POST /api/v1/pagos/webhook provienen de MercadoPago mediante la verificación del header `x-signature`. Si `MP_WEBHOOK_SECRET` está configurado (no vacío), la validación es OBLIGATORIA. Si no está configurado, se omite (solo para entornos de desarrollo local).

#### Scenario: Valid signature passes verification
- **WHEN** el webhook recibe una notificación con header `x-signature: ts=1742505638683,v1=abc123...`
- **AND** el HMAC SHA256 calculado con `MP_WEBHOOK_SECRET` y el manifest `id:{data.id};request-id:{x-request-id};ts:{ts};` coincide con `v1`
- **THEN** el sistema acepta la notificación y procede a procesarla

#### Scenario: Invalid or missing signature returns 401
- **WHEN** el webhook recibe una notificación SIN header `x-signature` (estando `MP_WEBHOOK_SECRET` configurado)
- **OR** el HMAC calculado NO coincide con `v1`
- **THEN** el sistema retorna HTTP 401 Unauthorized y NO procesa la notificación

#### Scenario: Signature validation skipped when secret is empty
- **WHEN** `MP_WEBHOOK_SECRET` está vacío o no configurado
- **THEN** el sistema omite la validación de firma y procesa la notificación normalmente (modo desarrollo)

### Requirement: HMAC signature computation follows MercadoPago documented algorithm
El sistema SHALL implementar exactamente el algoritmo documentado por MercadoPago: extraer `ts` y `v1` del header `x-signature`, construir el template `id:{data.id};request-id:{x-request-id};ts:{ts};` usando los valores de query params y headers, y calcular `HMAC-SHA256(secret, manifest)` en hexadecimal.

#### Scenario: Signature template construction
- **WHEN** el webhook recibe `?data.id=ORD01ABC123&type=payment` y headers `x-request-id: 2066ca19-c6f1-498a-be75` y `x-signature: ts=1742505638683,v1=ced36ab6...`
- **THEN** el sistema construye el manifest: `id:ord01abc123;request-id:2066ca19-c6f1-498a-be75;ts:1742505638683;`
- **AND** el `data.id` se convierte a minúsculas como requiere la documentación de MP

#### Scenario: Missing data.id query parameter
- **WHEN** el webhook recibe una notificación sin el query param `data.id`
- **AND** `MP_WEBHOOK_SECRET` está configurado
- **THEN** el sistema retorna 400 Bad Request indicando que falta `data.id`
