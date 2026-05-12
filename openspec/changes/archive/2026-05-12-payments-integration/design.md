## Context

El módulo `pedidos/` está implementado con FSM de 6 estados operativa. Los pedidos se crean en PENDIENTE pero no hay mecanismo para avanzarlos a CONFIRMADO — esa transición está reservada para el webhook de pagos (RN-FS02). El módulo `pagos/` existe como skeleton vacío (6 archivos de 2 líneas). La especificación técnica (`docs/Integrador.txt`) define el flujo completo de MercadoPago con PCI SAQ-A compliance, idempotency keys, y webhook IPN.

**Restricciones:**
- RN-FS02: PENDIENTE→CONFIRMADO solo automática vía pago aprobado
- RN-PA01: Datos de tarjeta tokenizados en browser, nunca en servidor
- RN-PA02: idempotency_key UUID único por pago
- RN-PA03: Webhook responde 200 inmediatamente
- RN-PA04: Siempre verificar estado real contra MP API
- RN-PA05: approved → CONFIRMADO + decremento stock atómico
- RN-PA08: Relación 1:N Pedido→Pago (múltiples intentos)
- RN-PA09: external_reference vincula preferencia MP con pedido

## Goals / Non-Goals

**Goals:**
- Implementar `POST /api/v1/pagos/crear` — crear preferencia MercadoPago y registrar Pago en BD
- Implementar `POST /api/v1/pagos/webhook` — recibir IPN, verificar firma, consultar MP API, actualizar estado
- Implementar `GET /api/v1/pagos/{pedido_id}` — consultar estado de pago (propietario/admin)
- Implementar `POST /api/v1/pagos/{pedido_id}/reintentar` — reintentar pago rechazado
- Transición automática PENDIENTE→CONFIRMADO con decremento de stock atómico en UoW
- Protección de idempotencia: webhooks duplicados se ignoran

**Non-Goals:**
- No se implementa frontend en este change (solo backend per scope del roadmap)
- No se implementa reembolso/cancelación de pagos aprobados
- No se configuran notificaciones push al cliente (solo webhook IPN)

## Decisions

### 1. SDK MercadoPago Python (mercadopago>=2.3.0)

**Alternativa considerada:** Hacer requests HTTP directos a la API REST de MP.

**Decisión:** Usar el SDK oficial `mercadopago`. Provee manejo de autenticación, reintentos y tipado. Es la dependencia especificada en el stack del proyecto (`docs/Integrador.txt`).

### 2. Modelo Pago: campos y relaciones

**Modelo elegido:**
```python
class Pago(SQLModel, table=True):
    id: int (PK)
    pedido_id: int (FK → pedidos.id, index)
    mp_payment_id: Optional[int] (UQ, NULL — ID devuelto por MP)
    idempotency_key: str (UQ — UUID generado al crear pago)
    external_reference: str (UQ — "{pedido_id}-{uuid_short}")
    status: str (pending | approved | rejected | in_process | cancelled | refunded)
    status_detail: Optional[str] 
    payment_method_id: Optional[str] (visa, master, rapipago, etc.)
    transaction_amount: float
    creado_en: datetime
    actualizado_en: datetime
```

**Justificación:** `idempotency_key` garantiza que un mismo pago no se procese dos veces (RN-PA02). `external_reference` es el puente entre MP y Food Store (RN-PA09). `mp_payment_id` puede ser NULL porque se asigna después de que MP responde.

### 3. Webhook: verificación de firma + consulta proactiva

**Decisión:** Dos pasos al recibir notificación IPN:
1. Verificar header `x-signature` contra `MP_WEBHOOK_SECRET` (si está configurado)
2. Siempre consultar `GET /v1/payments/{id}` a MP API para obtener el estado real (RN-PA04: nunca confiar solo en datos del webhook)

**Alternativa considerada:** Confiar ciegamente en los datos del webhook.

**Riesgo mitigado:** Un atacante podría enviar POST al webhook con datos falsos. La verificación de firma + consulta proactiva a MP previene esto.

### 4. Transición atómica: UoW con scope ampliado

**Decisión:** La confirmación de pago (`approved`) ejecuta en una única transacción UoW:
1. Actualizar `Pago.status = "approved"`, `Pago.mp_payment_id`
2. Actualizar `Pedido.estado_codigo = "CONFIRMADO"`
3. Insertar `HistorialEstadoPedido` (actor=SISTEMA)
4. Decrementar stock de cada `DetallePedido.producto_id`

Si cualquier paso falla → rollback completo. Esto garantiza que no quede un pedido CONFIRMADO sin stock decrementado, ni stock decrementado sin pedido confirmado.

### 5. Respuesta inmediata del webhook

**Decisión:** El endpoint webhook responde HTTP 200 inmediatamente después de validar la request y encolar el procesamiento. El procesamiento real (consulta MP API + transiciones) ocurre después de enviar la respuesta (RN-PA03).

**Alternativa considerada:** Procesar sincrónicamente dentro del request.

**Riesgo mitigado:** MercadoPago espera respuesta rápida; si tarda más de 10s, MP reenvía la notificación. Responder 200 ASAP evita reintentos innecesarios.

### 6. Pago con MercadoPago Orders API (no Preferences API legacy)

**Decisión:** Usar MercadoPago **Orders API** (`/v1/orders`) que es la API moderna recomendada para Checkout transparente, en lugar de la Preferences API legacy.

## Risks / Trade-offs

- **[Riesgo] Webhook no llega por problemas de red MP** → Mitigación: el frontend puede hacer polling periódico con GET /api/v1/pagos/{pedido_id} para detectar el estado real consultando MP API.
- **[Riesgo] Doble cobro si el webhook se procesa dos veces** → Mitigación: idempotency_key en BD; si ya existe pago aprobado para el pedido, se ignora.
- **[Riesgo] Stock negativo si dos pagos se confirman simultáneamente** → Mitigación: la UoW con isolation level READ COMMITTED + check de stock >= cantidad antes de decrementar.
- **[Trade-off] Procesamiento post-response del webhook** → Si el servidor crashea entre el 200 y el procesamiento real, el pago queda sin confirmar. Se mitiga con el polling del frontend que consulta MP API directamente.
- **[Riesgo] Med Risk en changelog-automation skill usada para reportar cambios** → No bloqueante, monitorear.
