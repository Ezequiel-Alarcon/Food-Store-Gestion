## Context

El módulo `pagos` implementa la integración con MercadoPago usando la Payment API (`sdk.payment().create()`). El webhook expone `POST /api/v1/pagos/webhook` como endpoint público para recibir notificaciones IPN. Actualmente el webhook procesa la notificación de forma **sincrónica** antes de responder y **no valida la firma criptográfica** `x-signature` que MP envía para autenticar la notificación.

La auditoría contra el Quality Checklist oficial de MP y la documentación de Webhooks identificó que el código actual no cumple con los estándares requeridos para producción.

## Goals / Non-Goals

**Goals:**
1. Validar criptográficamente las notificaciones webhook mediante HMAC SHA256 con `MP_WEBHOOK_SECRET`
2. Responder HTTP 200 inmediatamente y procesar en background dentro del timeout de 22s de MP
3. Enviar datos completos del payer (`email`, `first_name`, `last_name`, `identification`, `phone`) al crear pagos
4. Manejar errores de MP con tipos específicos (no `Exception` genérico)

**Non-Goals:**
- No se migra de Payment API a Checkout Pro/Preferences API
- No se implementan `items` individuales en el payment request (los productos ya están en el pedido)
- No se agregan `back_urls` (requiere frontend)
- No se implementa reintento automático con exponential backoff (requiere Celery/Redis)

## Decisions

### D1: Validación de firma — HMAC SHA256 según documentación oficial de MP

**Decisión**: Implementar exactamente el algoritmo documentado por MercadoPago para Webhooks:
1. Extraer `ts` y `v1` del header `x-signature` (formato: `ts=...,v1=...`)
2. Construir `manifest = f"id:{data.id};request-id:{x-request-id};ts:{ts};"`
3. Calcular `hmac.new(secret.encode(), manifest.encode(), sha256).hexdigest()`
4. Comparar con `v1`. Si no coinciden → 401.

**Alternativa considerada**: Usar una librería de terceros. Rechazada: el algoritmo es simple (<20 líneas), una dependencia extra no se justifica.

**Alcance**: La validación se aplica **solo si `MP_WEBHOOK_SECRET` está configurado** (no vacío). Esto permite desarrollo local sin secret.

### D2: Webhook asíncrono — FastAPI `BackgroundTasks`

**Decisión**: Usar `BackgroundTasks` de FastAPI para desacoplar la respuesta HTTP del procesamiento:
- El router recibe la notificación, valida la firma, y **si es válida** encola el procesamiento con `background_tasks.add_task(process_webhook, ...)`.
- Responde 200 inmediatamente.
- El procesamiento se ejecuta en un thread del pool de FastAPI (código síncrono de SQLAlchemy).

**Alternativa considerada**: `asyncio.create_task()`. Rechazada: el service de pagos es síncrono (SQLModel), no podemos meterlo en el event loop sin bloquear. BackgroundTasks lo ejecuta en thread pool automáticamente.

**Nota**: Cada invocación de `process_webhook` crea su propia `UnitOfWork(SessionLocal)` — no hay riesgo de sesión compartida.

### D3: Datos del payer — Obtener del modelo Usuario

**Decisión**: El `PagoService.crear_pago()` ya recibe `current_user`. Extender para obtener `email`, `nombre`, `apellido`, y `telefono` del usuario autenticado y enviarlos en el objeto `payer` del payment request a MP.

El objeto `payer` quedará:
```python
"payer": {
    "id": str(cliente_id),
    "email": current_user.email,
    "first_name": current_user.nombre,
    "last_name": current_user.apellido,
    "identification": {
        "type": "DNI",
        "number": current_user.documento or ""
    },
    "phone": {
        "number": current_user.telefono or ""
    }
}
```

Los campos `documento` y `telefono` son opcionales (pueden ser `None`/`""`), se omiten del request si no están disponibles.

### D4: Manejo de errores — Clasificación por tipo

**Decisión**: En lugar de `except Exception as e: raise ValidationError(...)`, clasificar:

| Tipo de error | Causa probable | HTTP Status |
|--------------|----------------|-------------|
| `mercadopago.error.MPError` con status 401 | Token inválido/expirado | 502 (error upstream) |
| `mercadopago.error.MPError` con status 429 | Rate limit de MP | 503 (retry-after) |
| `requests.exceptions.Timeout` | Timeout de red | 504 |
| `requests.exceptions.ConnectionError` | Sin conectividad | 502 |
| `ValidationError` / `NotFoundError` / `ForbiddenError` | Errores de dominio | Los que correspondan |

**Alternativa**: Seguir capturando `Exception`. Rechazada: imposibilita debugging y el cliente no puede reaccionar apropiadamente.

### D5: Rate limiting en webhook

**Decisión**: Agregar rate limit al endpoint `/pagos/webhook` usando `slowapi` (ya integrado). Límite: 60 req/min por IP. Esto previene DoS sin afectar notificaciones legítimas de MP (que tienen retry cada 15 min).

## Risks / Trade-offs

- **[Riesgo] BackgroundTasks no garantiza ejecución**: Si el proceso muere después del 200 pero antes de que BackgroundTasks termine, la notificación se pierde. → **Mitigación**: MP reenvía la notificación cada 15 min hasta 3 intentos. Si los 3 fallan, se escala a 1 intento por hora. Esto da margen de recuperación.
- **[Riesgo] Doble procesamiento por reenvío de MP**: Si BackgroundTasks está corriendo lento y MP reenvía, dos tareas procesan la misma notificación. → **Mitigación**: `procesar_webhook` ya es idempotente — verifica `pago.status == status` antes de actualizar (línea 152-153 actual). El `SELECT FOR UPDATE` previene race conditions a nivel BD.
- **[Trade-off] `MP_WEBHOOK_SECRET` vacío en desarrollo**: En desarrollo local sin secret configurado, el webhook no valida firma. Esto es aceptable para testing con ngrok/curl pero debe documentarse.

## Migration Plan

1. Crear branch `fix/payments-audit-fixes`
2. Implementar fixes en orden de criticidad: C1 (firma) → C2 (async) → A1 (payer data) → C3 (errores)
3. Probar webhook con ngrok + simulador de MP
4. Mergear a main
5. No requiere migración de BD ni cambios de schema

## Open Questions

- ¿Tenemos el `MP_WEBHOOK_SECRET` configurado en las credenciales de la app de MP? Si no, hay que generarlo en el panel de MP → Webhooks → Configurar notificaciones.
- ¿El modelo `Usuario` tiene campos `documento` y `telefono`? Verificar antes de implementar D3.
