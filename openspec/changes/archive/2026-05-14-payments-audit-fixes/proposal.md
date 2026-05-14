## Why

La auditoría del módulo de pagos contra el Quality Checklist oficial de MercadoPago reveló 3 bugs críticos de seguridad y confiabilidad, 4 problemas que impactan la tasa de aprobación, y 6 desvíos de buenas prácticas. El webhook de IPN acepta notificaciones sin validar firma criptográfica (cualquiera puede forzar transiciones de pedidos), procesa sincrónicamente antes de responder (riesgo de timeout y doble procesamiento), y no envía datos del payer a MP (baja tasa de aprobación). Estos problemas deben resolverse antes de considerar la integración productiva.

## What Changes

- **Validación de firma `x-signature` en webhook**: Implementar HMAC SHA256 con `MP_WEBHOOK_SECRET` para autenticar que las notificaciones provienen de MercadoPago. Rechazar con 401 las notificaciones sin firma o con firma inválida.
- **Webhook asíncrono**: Responder HTTP 200 inmediatamente al recibir el webhook, procesar la notificación en background (task asíncrono) para cumplir con el timeout de 22s de MP.
- **Datos del payer en payment request**: Enviar `payer.email`, `payer.first_name`, `payer.last_name`, `payer.identification`, y `payer.phone` al crear el pago. Estos datos mejoran la validación antifraude de MP y la tasa de aprobación.
- **Manejo de errores específico**: Diferenciar errores de red, autenticación MP, rate limiting, y validación. No capturar `Exception` genérico.
- **Configuración de rate limiting en webhook**: Proteger el endpoint público `/pagos/webhook` con rate limiting para evitar DoS.

## Capabilities

### New Capabilities
- `webhook-signature-validation`: Validación HMAC SHA256 de notificaciones webhook mediante header `x-signature` y `MP_WEBHOOK_SECRET`

### Modified Capabilities
- `payment-webhook`: El requerimiento "Receive MercadoPago IPN webhook" cambia para exigir procesamiento asíncrono real (no fire-and-forget sincrónico) y validación de firma obligatoria cuando `MP_WEBHOOK_SECRET` está configurado
- `payment-processing`: Se agrega el envío de datos completos del payer (`email`, `first_name`, `last_name`, `identification`, `phone`) al crear un pago, como campo obligatorio para mejorar la tasa de aprobación

## Impact

- `backend/app/modules/pagos/service.py` — Refactor de `procesar_webhook`, `crear_pago`, `reintentar_pago`, `_consultar_estado_mp`
- `backend/app/modules/pagos/router.py` — Webhook async + rate limiting
- `backend/app/modules/pagos/schemas.py` — Posible nuevo schema para datos del payer
- `backend/app/core/config.py` — `MP_WEBHOOK_SECRET` ya existe, solo se usará
- `backend/app/core/deps.py` — Posible rate limit para webhook
- `openspec/specs/payment-webhook/spec.md` — Delta spec
- `openspec/specs/payment-processing/spec.md` — Delta spec
