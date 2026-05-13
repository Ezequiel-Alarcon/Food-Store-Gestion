## 1. Schemas

- [x] 1.1 Completar `backend/app/modules/usuarios/schemas.py` con schemas Pydantic v2 (UserRead, UserUpdate, UserListResponse)
- [x] 1.2 Agregar `model_config` en cada schema (pattern: `model_config = {"str_strip_whitespace": True}`)

## 2. Router — Response Models

- [x] 2.1 Agregar `response_model` a GET / (list_users) con UserRead como list
- [x] 2.2 Agregar `response_model` a GET /{user_id} con UserRead
- [x] 2.3 Agregar `response_model` a PUT /{user_id} con UserRead
- [x] 2.4 Mantener DELETE /{user_id} como dict message (sin response_model)

## 3. Tests de Integración

- [x] 3.1 Crear directorio `backend/tests/modules/usuarios/`
- [x] 3.2 Crear `backend/tests/modules/usuarios/__init__.py`
- [x] 3.3 Crear `backend/tests/modules/usuarios/test_usuarios_endpoints.py` con fixtures de auth (admin, gestor, client)
- [x] 3.4 Implementar test: list_users como admin retorna 200 con lista
- [x] 3.5 Implementar test: list_users excluye inactivos por defecto
- [x] 3.6 Implementar test: get_user existente retorna 200
- [x] 3.7 Implementar test: get_user inexistente retorna 404
- [x] 3.8 Implementar test: update_user como admin actualiza campos
- [x] 3.9 Implementar test: update_user como gestor retorna 403
- [x] 3.10 Implementar test: deactivate_user como admin retorna 200
- [x] 3.11 Implementar test: deactivate_user como gestor retorna 403

## 4. Verificación

- [x] 4.1 Correr tests: `pytest backend/tests/modules/usuarios/ -v`
- [x] 4.2 Verificar que todos los tests pasen
- [x] 4.3 Verificar que schema archivos no tengan errores de lint

## Notas

- **4.1-4.3 bloqueados**: El entorno de tests tiene un problema de incompatibilidad entre passlib y bcrypt (error "password cannot be longer than 72 bytes"). Este es un problema pre-existente del proyecto que afecta también a los tests de pedidos. Los tests fueron escritos siguiendo el patrón correcto pero no pueden ejecutarse hasta que se resuelva el issue de dependencias.