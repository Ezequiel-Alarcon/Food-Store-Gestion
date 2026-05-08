## Context

El proyecto Food Store requiere un sistema de autenticación para permitir que los usuarios se identifiquen, protejan recursos, y manejen roles. El change 5 (error-handling) ya está archivado y el change 4 (backend-patterns) estableció BaseRepository, UnitOfWork, y las dependencias de seguridad básicas.

**Estado actual del código:**
- ✅ `backend/app/modules/auth/schemas.py` — **COMPLETO** (RegisterRequest, LoginRequest, TokenResponse, etc.)
- ✅ `backend/app/core/security.py` — **COMPLETO** (hash_password bcrypt cost 12, create_access_token, create_refresh_token, decode_token)
- ✅ `backend/app/core/deps.py` — **COMPLETO** (get_current_user, require_role)
- ✅ `backend/app/core/config.py` — **COMPLETO** (JWT settings, rate limits)
- ✅ `backend/app/main.py` — skeleton con routers comentados

**Por implementar:**
- Modelos: Usuario, RefreshToken
- Repository: auth, usuarios, refreshtokens
- Service: lógica de negocio
- Router: endpoints operativos
- Integración en main.py

## Goals / Non-Goals

**Goals:**
- Implementar register, login, refresh, logout con JWT
- CRUD de usuarios por ADMIN/GESTOR
- Gestión de perfil propio (ver, editar, cambiar password)
- Sistema de RBAC con roles ADMIN/GESTOR/CLIENT
- Rate limiting en endpoints de auth (5 intentos/15min por IP)

**Non-Goals:**
- OAuth social (Google, Facebook) — queda para future work
- 2FA/MFA — queda para future work
- Frontend de autenticación — es el change 7 (`auth-frontend`)
- Password reset por email — queda para future work

## Decisions

### 1. JWT Strategy: Access Token (15min) + Refresh Token (7 días)

**Decision:** Access token corto para minimizar daño si es robado, refresh token longo para UX.

- Access token: 15 minutos, contenido en payload (no BBDD)
- Refresh token: 7 días, almacenado en PostgreSQL con campo `revocado` boolean

**Alternativa considerada:**
- Token único longo (30 días): descartado por seguridad — un token robado dura demasiado
- Single token con refresh flag: complejiza validación, requiere lookup en BBDD cada request

### 2. Refresh Token Storage: PostgreSQL (no Redis)

**Decision:** Almacenar refresh tokens en tabla `refresh_tokens` de PostgreSQL.

**Alternativa considerada:**
- Redis: más rápido, pero agregaría infraestructura. PostgreSQL es suficiente para el volumen esperado.
- JWT refresh token (stateless): no permite invalidación inmediata ni token rotation práctico.

**Trade-off:** Cada refresh requiere 1 query a BBDD. Aceptable para MVP.

### 3. Password Hashing: bcrypt con cost 12

**Decision:** Usar bcrypt con el parámetro rounds=12 para balance seguridad/rendimiento.

**Alternativa considerada:**
- Argon2: más seguro pero más lento, require instalar library adicional
- scrypt: opción buena pero menos estándar en Python

### 4. RBAC Implementation: Dependency injection + Decorator

**Decision:** Dos mecanismos complementarios:
- `require_role(allowed_roles: list[str])` como dependency de FastAPI
- Decorador `@require_roles()` para endpoints individuales

**Alternativa considerada:**
- Middleware global: muy inflexible,需要对每条路径单独配置
- Solo decorators: no permite verificación rápida en dependencies

### 5. Perfil Management: Endpoints dedicados bajo /api/v1/perfil

**Decision:** Crear router dedicado para perfil propio del usuario autenticado.

**Alternativa considerada:**
- endpoints en `/api/v1/usuarios/me`: mezcla concerns con CRUD de admin

**Trade-off:** Duplicación menor de lógica vs. separación clara de concerns.

## Risks / Trade-offs

- **[Risk]** Refresh token attacks (token theft) → [Mitigation] Implementar token rotation (nuevo refresh en cada uso) + invalidación al cambiar password

- **[Risk]** Rate limiting puede bloquear múltiples usuarios tras NAT → [Mitigation] Limit por IP es suficiente para MVP; en producción considerar login por email como key

- **[Risk]** JWT tokens no pueden ser revocados antes de expirar → [Mitigation] Access tokens cortos (15min); refresh tokens pueden ser revocados individualmente

- **[Risk]** Sincronización de clocks entre servidores → [Mitigation] Usar timedelta de datetime, no time.time() absolutos

## Open Questions

- ¿El endpoint de logout debe aceptar refresh token en body o header? → **Decision:** Aceptar ambos (body más compatible con mobile)
- ¿ElADMIN puede ver passwords de usuarios? → **Decision:** NO, hash no es visible ni restaurable
- ¿Cuántos refresh tokens activos por usuario? → **Decision:** Múltiples permitidos (multi-device), invalidar todos al cambiar password

## Migration Plan

1. Crear tablas necesarias (migración Alembic: añadir columnas faltantes a `usuarios` y `refresh_tokens` si aplica)
2. Deploy del nuevo módulo `modules/auth/` y `modules/usuarios/`
3. Endpoints de auth quedan abiertos (públicos), endpoints de perfil requieren auth
4. No hay breaking changes — no hay código existente que dependa de auth

## Schema de API

```
POST   /api/v1/auth/register     (público)
POST   /api/v1/auth/login       (público, rate limited)
POST   /api/v1/auth/refresh     (público)
POST   /api/v1/auth/logout      (autenticado)

GET    /api/v1/usuarios         (ADMIN/GESTOR)
GET    /api/v1/usuarios/{id}    (ADMIN/GESTOR)
PUT    /api/v1/usuarios/{id}    (ADMIN)
DELETE /api/v1/usuarios/{id}    (ADMIN)

GET    /api/v1/perfil           (autenticado)
PUT    /api/v1/perfil           (autenticado)
PUT    /api/v1/perfil/password  (autenticado)
```