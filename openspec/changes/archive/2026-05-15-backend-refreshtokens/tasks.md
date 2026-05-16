## 1. Schemas Pydantic

- [x] 1.1 Crear `schemas.py` con `RefreshTokenRead` (id, user_id, expires_at, created_at, revocado)
- [x] 1.2 Crear `schemas.py` con `RefreshTokenListResponse` (lista de RefreshTokenRead + count)
- [x] 1.3 Crear `schemas.py` con `RevokeResponse` (id, user_id, message)
- [x] 1.4 Crear `schemas.py` con `BulkRevokeResponse` (user_id, revoked_count, message)

## 2. Refactorizar Service para usar Unit of Work

- [x] 2.1 Refactorizar `RefreshTokenService.__init__` para recibir `UnitOfWork` en lugar de `Session`
- [x] 2.2 Refactorizar `RefreshTokenService.create` para usar `with uow:` context manager
- [x] 2.3 Refactorizar `RefreshTokenService.revoke` para usar `with uow:` context manager
- [x] 2.4 Refactorizar `RefreshTokenService.revoke_all_by_user` para usar `with uow:` context manager
- [x] 2.5 Mantener `get_valid` sin UoW (solo lectura, usa repo directamente con session pasada como parámetro)

## 3. Completar Router

- [x] 3.1 Crear `router.py` con APIRouter(prefix="/refreshtokens", tags=["refreshtokens"])
- [x] 3.2 Implementar GET `/user/{user_id}` — listar tokens activos (admin-only, usa require_role)
- [x] 3.3 Implementar POST `/revoke/{token_id}` — revocar token individual (admin-only)
- [x] 3.4 Implementar DELETE `/user/{user_id}/all` — revocar todos los tokens de un usuario (admin-only)
- [x] 3.5 Agregar imports de deps: `require_current_user`, `require_role`, `UnitOfWork`

## 4. Registrar módulo en main.py

- [x] 4.1 Agregar import `from app.modules.refreshtokens.router import router as refreshtokens_router`
- [x] 4.2 Agregar `app.include_router(refreshtokens_router, prefix="/api/v1", tags=["refreshtokens"])`

## 5. Completar __init__.py

- [x] 5.1 Exportar clases públicas: `RefreshToken`, `RefreshTokenRepository`, `RefreshTokenService`, `router`

## 6. Agregar índice en columna token

- [x] 6.1 Modificar `model.py` — agregar `index=True` al campo `token`
- [x] 6.2 Generar migración Alembic `008_add_index_refresh_tokens_token.py`

## 7. Tests

- [x] 7.1 Crear directorio `backend/tests/modules/refreshtokens/` con `__init__.py`
- [x] 7.2 Crear `test_repository.py` — tests para RefreshTokenRepository (create, get_valid, revoke, revoke_all)
- [x] 7.3 Crear `test_service.py` — tests para RefreshTokenService con UoW
- [x] 7.4 Crear `test_endpoints.py` — tests de integración para los 3 endpoints (list, revoke, bulk revoke)
- [x] 7.5 Crear `test_endpoints.py` — tests de autorización (403 para no-admin, 401 para no-auth)
