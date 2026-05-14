## Why

El módulo de pagos backend (`pagos/`) funciona correctamente con el token TEST de MercadoPago (verificado con pago Rapipago). Sin embargo, para pagos con tarjeta de crédito/débito se necesita un frontend que tokenice la tarjeta mediante `@mercadopago/sdk-react` y envíe el `token` al endpoint `POST /api/v1/pagos/crear`. Sin esto, no se puede probar el flujo completo de pago con tarjetas ni cumplir con la especificación PCI SAQ-A.

## What Changes

- **Nueva página de checkout**: `frontend/src/features/checkout/` con formulario de pago que integra `@mercadopago/sdk-react` para tokenización de tarjeta
- **Integración con backend**: Llamar a `POST /api/v1/pagos/crear` con `payment_method_id` + `token` de tarjeta
- **Flujo post-pago**: Mostrar resultado (éxito/rechazo/pendiente) y redirigir a detalle del pedido

## Capabilities

### New Capabilities
- `checkout-card-payment`: Tokenización de tarjeta en frontend con `@mercadopago/sdk-react` y envío al backend

## Impact

- `frontend/src/features/checkout/` — nueva feature FSD
- `frontend/src/entities/pago/` — API client, types
- `frontend/package.json` — agregar `@mercadopago/sdk-react`
