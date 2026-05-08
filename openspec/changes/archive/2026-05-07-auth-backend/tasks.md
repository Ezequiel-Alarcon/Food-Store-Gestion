## 1. Modelos (Database)

- [x] 1.1 Crear `backend/app/modules/auth/model.py` — Modelo Usuario (SQLModel) con campos: id, email, nombre, password_hash, rol, telefono, activo, created_at, updated_at
- [x] 1.2 Crear `backend/app/modules/refreshtokens/model.py` — Modelo RefreshToken (SQLModel) con campos: id, user_id, token, revocado, expires_at, created_at
- [x] 1.3 Ejecutar migración Alembic para crear las tablas

## 2. Repository

- [x] 2.1 Implementar `backend/app/modules/auth/repository.py` — AuthRepository con métodos: create_user, get_user_by_email, get_user_by_id, verify_password
- [x] 2.2 Implementar `backend/app/modules/refreshtokens/repository.py` — RefreshTokenRepository con métodos: create, get_by_token, revoke, revoke_all_by_user
- [x] 2.3 Crear `backend/app/modules/usuarios/repository.py` — UsuariosRepository con métodos: get_all, get_by_id, update, delete (para ADMIN)

## 3. Service

- [x] 3.1 Implementar `backend/app/modules/auth/service.py` — AuthService: register, login, verify_password, create_token_pair
- [x] 3.2 Implementar `backend/app/modules/refreshtokens/service.py` — RefreshTokenService: create, refresh, revoke, revoke_all
- [x] 3.3 Crear `backend/app/modules/usuarios/service.py` — UsuariosService con lógica CRUD para admin (GESTOR puede ver)
- [x] 3.4 Crear `backend/app/modules/perfil/service.py` — PerfilService: get_perfil, update_perfil, change_password

## 4. Router

- [x] 4.1 Implementar `backend/app/modules/auth/router.py` — Endpoints: POST /register, POST /login, POST /refresh, POST /logout (rate limited en /login)
- [x] 4.2 Crear `backend/app/modules/usuarios/router.py` — Endpoints: GET / (ADMIN/GESTOR), GET /{id}, PUT /{id} (ADMIN), DELETE /{id} (ADMIN)
- [x] 4.3 Crear `backend/app/modules/perfil/router.py` — Endpoints: GET /perfil, PUT /perfil, PUT /perfil/password

## 5. Main Integration

- [x] 5.1 Descomentar imports de routers en `backend/app/main.py`
- [x] 5.2 Registrar auth_router, usuarios_router, perfil_router con prefijo /api/v1
- [x] 5.3 Aplicar rate limiting al endpoint /login

## 6. Tests

- [x] 6.1 Crear `backend/tests/test_auth_service.py` — Tests unitarios para AuthService
- [x] 6.2 Crear `backend/tests/test_auth_endpoints.py` — Tests de integración para /auth/register y /auth/login
- [x] 6.3 Crear `backend/tests/test_perfil_endpoints.py` — Tests de integración para endpoints de perfil

## 7. Documentation

- [x] 7.1 Agregar docstrings a los módulos auth, usuarios, perfil, refreshtokens
- [x] 7.2 Verificar que OpenAPI genere correctamente los esquemas en /docs