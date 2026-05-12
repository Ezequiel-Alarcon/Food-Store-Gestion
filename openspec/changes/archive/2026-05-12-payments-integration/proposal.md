## Why

El módulo de pedidos (`pedidos/`) ya permite crear órdenes en estado PENDIENTE, pero no existe integración de pagos. Sin procesamiento de pagos, las órdenes quedan estancadas en PENDIENTE para siempre — la FSM no puede avanzar a CONFIRMADO porque esa transición es exclusivamente automática vía pago aprobado (RN-FS02). Food Store necesita cerrar el flujo de compra integrando MercadoPago Checkout API para que los clientes puedan pagar y el sistema avance los pedidos automáticamente.

## What Changes

- Implementar `POST /api/v1/pagos/crear` — crear preferencia de pago en MercadoPago con idempotency_key UUID
- Implementar `POST /api/v1/pagos/webhook` — endpoint IPN que recibe notificaciones de MercadoPago, verifica firma y actualiza estado del pago y pedido
- Implementar `GET /api/v1/pagos/{pedido_id}` — consultar estado de pago de un pedido (propietario/admin)
- Implementar `POST /api/v1/pagos/{pedido_id}/reintentar` — reintentar pago rechazado con nuevo idempotency_key
- Transición automática PENDIENTE→CONFIRMADO cuando el webhook recibe `approved`, con decremento atómico de stock (RN-PA05)
- Relación 1:N Pedido→Pago: un pedido puede tener múltiples intentos de pago (RN-PA08)
- Los datos de tarjeta NUNCA tocan el servidor — se tokenizan en el frontend vía SDK MercadoPago.js (PCI SAQ-A)
- Variables de entorno: `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY`, `MP_NOTIFICATION_URL`

## Capabilities

### New Capabilities
- `payment-processing`: Creación de preferencias de pago via MercadoPago Orders API, idempotency key, registro en tabla Pago, vinculación con pedido via external_reference.
- `payment-webhook`: Recepción y procesamiento de notificaciones IPN de MercadoPago. Verificación de firma, consulta de estado real a MP API (nunca confiar solo en datos del webhook), respuesta HTTP 200 inmediata.
- `payment-status`: Consulta del estado de pago asociado a un pedido. Solo propietario o admin pueden consultar.
- `payment-retry`: Reintento de pago cuando el anterior fue rechazado. Genera nuevo idempotency_key y nueva preferencia en MP. El pedido permanece en PENDIENTE.

### Modified Capabilities
- `order-transitions`: La transición PENDIENTE→CONFIRMADO ahora se dispara desde el webhook de pago (no manualmente). Al confirmar, se decrementa atómicamente el stock de cada producto del pedido. Se agrega el método `confirmar_pedido()` en el servicio de pedidos.

## Impact

- `backend/app/modules/pagos/` — implementación completa: model, schemas, repository, service, router (actualmente skeletons vacíos)
- `backend/app/modules/pedidos/service.py` — nuevo método `confirmar_pedido(pedido_id)` llamado por el webhook
- `backend/app/modules/productos/service.py` — nuevo método `decrementar_stock(producto_id, cantidad)` para la confirmación atómica
- `backend/app/core/config.py` — nuevas variables de entorno para MercadoPago
- `.env.example` — documentar `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY`, `MP_NOTIFICATION_URL`
- `backend/requirements.txt` — verificar/agregar `mercadopago>=2.3.0`
- `backend/app/db/migrations/versions/` — nueva migración para tabla `pago`
