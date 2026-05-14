## Why

Tres bugs críticos de seguridad y consistencia fueron identificados durante code review del codebase backend. Si no se corrigen, pueden causar: fallo en login con emails mayúsculas/minúsculas, pérdida de sesiones de usuario durante refresh token, y comportamiento impredecible con timezones en producción. Adicionalmente, una violación de arquitectura en el admin router compromete el patrón Router→Service→UoW→Repository→Model.

## What Changes

- **BUG-1 Fix**: Normalizar email a lowercase en `get_user_by_email_optional` (auth/repository.py) para consistencia con el resto del flujo auth
- **BUG-2 Fix**: Envolver token rotation en transacción atómica usando UoW (auth/service.py)
- **BUG-3 Fix**: Reemplazar todos los `datetime.utcnow()` por `datetime.now(timezone.utc)` en pedidos/service.py y auth/service.py
- **ARQ-1 Fix**: Mover lógica de queries del admin/router.py a PedidosService siguiendo el patrón de arquitectura
- **ARQ-3 Fix**: Reemplazar HTTPException por AppError en auth/service.py (servicios deben lanzar errores de dominio, no HTTP)

## Capabilities

### New Capabilities

- _(Ninguna — estos son fixes de bugs existentes, no neue funcionalidades)_

### Modified Capabilities

- `auth`: Corrección de normalización de email y transacción de token rotation — afecta el behavior existente de login/refresh
- `pedidos`: Unificación de timezone handling — afecta timestamps en estados de pedido
- `admin`: Corrección de arquitectura — mueve lógica de HTTP a Service layer

## Impact

**Backend:**
- `app/modules/auth/repository.py` — normalización de email en `get_user_by_email_optional`
- `app/modules/auth/service.py` — transacción atómica en `_rotate_token_pair`
- `app/modules/pedidos/service.py` — reemplazo `datetime.utcnow()` → `datetime.now(timezone.utc)`
- `app/modules/auth/service.py` — reemplazo `datetime.utcnow()` → `datetime.now(timezone.utc)`
- `app/modules/admin/router.py` — extracción de queries a PedidosService
- `app/core/exceptions.py` — verificar que AppError esté correctamente definido para uso en servicios

**Tests:**
- Verificar que los tests existentes de auth siguen pasando después del fix de email normalization
- Verificar que los tests de pedidos siguen pasando después del fix de timezone