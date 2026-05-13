## Why

La auditoría de autenticación reveló 22 bugs en el módulo auth — 6 críticos, 5 high — que impiden el flujo de autenticación end-to-end. El Swagger pide `client_id`/`client_secret` inexistentes (BUG #1), el seed de datos está completamente roto (BUG #2, #3), hay roles faltantes (BUG #4), y existen vulnerabilidades de seguridad como filtrado de información en login (BUG #9) y refresh tokens utilizables por usuarios desactivados (BUG #8). El proyecto está en deuda técnica con su propia especificación v5.0 (docs/Integrador.txt).

## What Changes

- **Swagger/OAS**: Reemplazar `OAuth2PasswordBearer(tokenUrl="token")` por configuración correcta que muestre un simple campo para pegar token JWT, sin formulario OAuth2
- **Modelo Usuario**: Agregar campo `apellido` requerido por los docs (RegisterRequest, UserResponse), alinear nombres de campos (`created_at` → `creado_en`)
- **RBAC**: Agregar roles STOCK y PEDIDOS faltantes en `RolEnum` (actualmente solo 3 de 4), usar `RolEnum` para validación de roles en schemas
- **Seed data**: Hacer que funcione con los modelos reales (sin `Rol` ni `UsuarioRol` inexistentes), crear usuario admin correctamente
- **Login**: Eliminar filtración de info ("Usuario desactivado" → mensaje genérico), alinear rate limit docs (5/15min vs 5/min)
- **Refresh token**: Agregar chequeo `usuario.activo`, corregir orden de operaciones (no revocar antes de verificar usuario)
- **Password change**: Invalidar TODOS los refresh tokens al cambiar contraseña (RN-AU05, US-063)
- **Cambio de contraseña**: Validar que nueva != actual, invalidar todos los refresh tokens
- **Tokens JWT**: Agregar `type: "access"` al payload del access token, consistencia con `get_current_user`
- **Datetime**: Migrar de `datetime.utcnow()` (naive) a `datetime.now(timezone.utc)` (aware) en modelos y repositorios
- **Validación password**: Agregar validadores de complejidad (1 mayúscula, 1 número) prometidos en el schema pero no implementados
- **Rate limiting**: Agregar `SlowAPIMiddleware` faltante (actualmente el rate limiting está inactivo)
- **response_model**: Agregar `response_model` explícito en 5 endpoints que no lo tienen
- **Config**: Sincronizar defaults entre `.env.example` y `config.py` (ACCESS_TOKEN_EXPIRE_MINUTES: 15→30)

## Capabilities

### New Capabilities
- `auth-seed-data`: Seed de datos de auth que funciona con los modelos reales — roles + usuario admin con credenciales configurables
- `auth-swagger-config`: Configuración Swagger/OpenAPI para autenticación JWT — sin formulario OAuth2, solo campo para Bearer token

### Modified Capabilities
- `user-login`: Fix info leak (RN-AU08), alinear rate limit docs (5/15min), corregir tokenUrl Swagger, agregar type:access al JWT
- `user-registration`: Agregar campo `apellido` a RegisterRequest (docs v5.0), agregar validación de complejidad de password, corregir `nombre_not_whitespace` return value
- `token-refresh`: Chequear `usuario.activo` antes de emitir nuevos tokens, corregir orden revoke→verify, migrar a datetime aware
- `role-based-access`: Completar `RolEnum` con 4 roles (STOCK, PEDIDOS), usar enum para validación en schemas
- `auth-dependencies`: `OAuth2PasswordBearer` → `HTTPBearer`, eliminar formulario OAuth2 falso en Swagger
- `password-change`: Invalidar todos los refresh tokens del usuario (no solo el actual), agregar validación new_password ≠ current_password
- `rate-limiting`: Agregar `SlowAPIMiddleware` para que el rate limiting funcione, alinear constantes con docs

## Impact

- **Archivos backend modificados**: `deps.py`, `config.py`, `security.py`, `auth/model.py`, `auth/schemas.py`, `auth/service.py`, `auth/router.py`, `auth/repository.py`, `db/seed.py`, `main.py`, `perfil/service.py`, `refreshtokens/repository.py`
- **Archivos backend nuevos**: ninguno (solo modificaciones)
- **Migraciones**: nueva migración para agregar campo `apellido` a tabla `usuarios`, cambiar `created_at`/`updated_at` a `TIMESTAMPTZ`
- **Frontend**: sin impacto (cambio backend-only)
- **Breaking changes**: 
  - `RegisterRequest` ahora requiere `apellido` (**BREAKING** para clientes que no lo envían)
  - `TokenResponse` puede incluir `expires_in` con nuevo valor (30 min en vez de 15)
  - `RolEnum.GESTOR` → los docs usan `STOCK` y `PEDIDOS`; si hay código referenciando `GESTOR` hay que actualizarlo
