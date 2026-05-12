## 1. Modelo y Migración

- [x] 1.1 Crear modelo `Pago` en `backend/app/modules/pagos/model.py` con campos: id (PK), pedido_id (FK), mp_payment_id (UQ, nullable), idempotency_key (UQ), external_reference (UQ), status, status_detail, payment_method_id, transaction_amount, creado_en, actualizado_en
- [x] 1.2 Generar migración Alembic para tabla `pagos` con `alembic revision --autogenerate -m "add_pagos_table"` y verificar que el script de migración sea correcto
- [x] 1.3 Agregar índice en `pedido_id` para búsquedas por pedido

## 2. Schemas Pydantic

- [x] 2.1 Crear `PagoCreate` schema (pedido_id) en `schemas.py`
- [x] 2.2 Crear `PagoResponse` schema (id, pedido_id, mp_payment_id, idempotency_key, external_reference, status, status_detail, payment_method_id, transaction_amount, creado_en, actualizado_en)
- [x] 2.3 Crear `WebhookPayload` schema (topic, resource_id) para validación del webhook entrante

## 3. Configuración MercadoPago

- [x] 3.1 Agregar variables de entorno en `.env.example`: `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY`, `MP_NOTIFICATION_URL`, `MP_WEBHOOK_SECRET` (opcional)
- [x] 3.2 Agregar settings en `backend/app/core/config.py`: `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY`, `MP_NOTIFICATION_URL`, `MP_WEBHOOK_SECRET`
- [x] 3.3 Verificar que `mercadopago>=2.3.0` está en `requirements.txt`; si no, agregarlo

## 4. Repository

- [x] 4.1 Crear `PagoRepository` en `repository.py` extendiendo `BaseRepository[Pago]`
- [x] 4.2 Implementar `find_by_pedido_id(pedido_id)` — retorna lista de pagos del pedido (ordenados por creado_en DESC)
- [x] 4.3 Implementar `find_by_idempotency_key(key)` — buscar pago por idempotency_key para chequeo de duplicados
- [x] 4.4 Implementar `find_latest_by_pedido_id(pedido_id)` — retorna el último pago del pedido

## 5. Service — Creación de Pago

- [x] 5.1 Implementar `PagoService.crear_pago(pedido_id, cliente_id)` — valida que el pedido esté en PENDIENTE y pertenezca al cliente, genera idempotency_key UUID, crea orden en MercadoPago Orders API, persiste Pago con status="pending", retorna datos de preferencia
- [x] 5.2 Implementar helper `_generar_external_reference(pedido_id)` — formato "pedido-{id}-{uuid8}"
- [x] 5.3 Manejar errores de MP API (timeout, 4xx, 5xx) con logging y HTTPException apropiada

## 6. Service — Webhook IPN

- [x] 6.1 Implementar `PagoService.procesar_webhook(topic, resource_id)` — si topic != "payment", ignorar
- [x] 6.2 Implementar verificación de firma `x-signature` contra `MP_WEBHOOK_SECRET` (si está configurado)
- [x] 6.3 Implementar `_verificar_estado_mp(mp_payment_id)` — consulta GET /v1/payments/{id} a MP API para obtener estado real (RN-PA04)
- [x] 6.4 Implementar `PagoService.confirmar_pago(pago)` — caso approved: actualiza Pago, transiciona Pedido a CONFIRMADO via UoW, decrementa stock, inserta HistorialEstadoPedido con actor=SISTEMA (todo en una transacción)
- [x] 6.5 Implementar casos rejected/pending/in_process — actualizar Pago.status y Pago.status_detail, pedido sigue PENDIENTE
- [x] 6.6 Proteger idempotencia: si el pago ya fue procesado (mismo mp_payment_id), no hacer nada

## 7. Productos — Decremento de Stock

- [x] 7.1 Agregar método `decrementar_stock(producto_id, cantidad)` en `backend/app/modules/productos/service.py` que verifica stock suficiente y decrementa
- [x] 7.2 Lanzar `ValidationError` si stock insuficiente (la UoW hará rollback en `confirmar_pago`)

## 8. Pedidos — Confirmación desde Webhook

- [x] 8.1 Agregar método `confirmar_pedido(pedido_id, uow)` en `backend/app/modules/pedidos/service.py` que valida transición PENDIENTE→CONFIRMADO, actualiza estado, e inserta HistorialEstadoPedido con actor=SISTEMA
- [x] 8.2 El FSM debe permitir la transición PENDIENTE→CONFIRMADO cuando es ejecutada por el sistema (no por usuario)

## 9. Router — Endpoints

- [x] 9.1 Implementar `POST /api/v1/pagos/crear` — crea pago (protegido: requiere auth, solo CLIENT propietario)
- [x] 9.2 Implementar `POST /api/v1/pagos/webhook` — endpoint público (sin auth), recibe IPN de MP, retorna 200 inmediato, procesa async
- [x] 9.3 Implementar `GET /api/v1/pagos/{pedido_id}` — consulta estado de pago (propietario o ADMIN)
- [x] 9.4 Implementar `POST /api/v1/pagos/{pedido_id}/reintentar` — reintenta pago rechazado (CLIENT propietario, pedido PENDIENTE, último pago rejected)
- [x] 9.5 Usar `response_model` explícito en todos los endpoints

## 10. Integración y Wiring

- [x] 10.1 Incluir el router de pagos en `backend/app/main.py` (si existe registro centralizado de routers)
- [x] 10.2 Agregar seed data para formas de pago si no existe (verificar `backend/app/db/seed.py`)
- [x] 10.3 Verificar que el módulo no rompe imports circulares (pagos → pedidos/productos debe pasar por services, no models)

## 11. Pruebas Manuales

- [x] 11.1 Probar flujo completo: crear pedido → POST /pagos/crear → simular webhook approved → verificar pedido CONFIRMADO y stock decrementado
- [x] 11.2 Probar caso rechazo: webhook rejected → pedido sigue PENDIENTE → reintentar pago → nuevo pago creado
- [x] 11.3 Probar idempotencia: mismo webhook dos veces → solo se procesa una vez
- [x] 11.4 Probar permisos: cliente ajeno no puede pagar ni consultar pedido de otro
