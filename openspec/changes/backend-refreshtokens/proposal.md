## Why

El módulo `refreshtokens` fue scaffolded pero nunca completado. Los archivos `router.py` y `schemas.py` están vacíos, el módulo no está registrado en `main.py`, y no tiene tests. Aunque el flujo de refresh funciona actualmente a través del módulo `auth`, el módulo `refreshtokens` debería ser un componente standalone con endpoints propios para gestión administrativa de tokens (listar, revocar, auditar).

## What Changes

- Completar `schemas.py` con schemas Pydantic para request/response de gestión de refresh tokens
- Completar `router.py` con endpoints protegidos (admin-only) para listar y revocar tokens
- Refactorizar `service.py` para usar el patrón Unit of Work (actualmente opera sin UoW)
- Registrar el router en `main.py` con prefijo `/api/v1/refreshtokens`
- Exportar clases públicas en `__init__.py`
- Agregar índice en columna `token` del modelo para optimizar búsquedas
- Crear tests de integración para el módulo completo

## Capabilities

### New Capabilities
- `refresh-token-admin`: Endpoints administrativos para gestión de refresh tokens — listar tokens activos por usuario, revocar token individual, revocar todos los tokens de un usuario.

### Modified Capabilities
<!-- No existing specs change their requirements — this adds admin capabilities on top of the existing token-refresh flow -->

## Impact

- **Backend**: `backend/app/modules/refreshtokens/` (router.py, schemas.py, service.py, __init__.py), `backend/app/main.py` (registro de router), `backend/app/modules/refreshtokens/model.py` (agregar índice)
- **Tests**: Nuevos archivos en `backend/tests/modules/refreshtokens/`
- **API**: Nuevos endpoints bajo `/api/v1/refreshtokens/` (protegidos, admin-only)
- **Frontend**: Sin cambios — el flujo de refresh actual sigue operando a través de `/auth/refresh`
