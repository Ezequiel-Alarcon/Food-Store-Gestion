## 1. Email Normalization Fix

- [ ] 1.1 Normalizar email en `get_user_by_email_optional` (`auth/repository.py`) — agregar `.lower()` al where clause
- [ ] 1.2 Verificar que `get_user_by_email` ya normaliza (si no, normalizar también)
- [ ] 1.3 Correr tests de auth para verificar que el fix no rompe nada

## 2. Token Rotation Atomic Transaction

- [ ] 2.1 Implementar try-except en `_rotate_token_pair` (`auth/service.py`) para rollback si `_create_token_pair` falla
- [ ] 2.2 Agregar log de error en el except para debugging
- [ ] 2.3 Testear manualmente el flujo de refresh token

## 3. Timezone Normalization

- [ ] 3.1 Reemplazar `datetime.utcnow()` por `datetime.now(timezone.utc)` en `pedidos/service.py`
- [ ] 3.2 Reemplazar `datetime.utcnow()` por `datetime.now(timezone.utc)` en `auth/service.py`
- [ ] 3.3 Importar `timezone` from `datetime` si no está importado
- [ ] 3.4 Correr tests de pedidos para verificar timestamps

## 4. Admin Router Architecture Fix

- [ ] 4.1 Crear método `list_pedidos_for_admin` en `PedidosService` que contenga la lógica de queries del admin router
- [ ] 4.2 Refactorizar `admin/router.py` para usar `PedidosService.list_pedidos_for_admin()` en lugar de queries directas
- [ ] 4.3 Verificar que los tests de admin metrics siguen pasando

## 5. HTTPException → AppError

- [ ] 5.1 Revisar `app/core/exceptions.py` para ver AppError subclasses disponibles
- [ ] 5.2 Reemplazar HTTPException por AppError (o subclass) en `auth/service.py`
- [ ] 5.3 Si no existe InvalidCredentialsError, usar uno genérico o crear el subclass

## 6. Verification

- [ ] 6.1 Correr todos los tests del backend (`python -m pytest tests/ -v`)
- [ ] 6.2 Verificar que 68/68 tests pasan
- [ ] 6.3 Commitear cambios con conventional commits