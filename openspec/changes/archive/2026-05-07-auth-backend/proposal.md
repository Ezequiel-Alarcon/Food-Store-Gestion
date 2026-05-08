## Why

El sistema actualmente carece de un módulo de autenticación robusto. Sin register, login, ni gestión de usuarios, no hay forma de identificar clientes ni proteger recursos. El proyecto necesita identidad para mover pedidos, perfiles, y roles desde el Sprint 1.

## What Changes

- **Módulo auth**: Endpoints de register, login, logout, refresh token con JWT
- **Módulo usuarios**: CRUD completo + gestión de roles (CLIENT, GESTOR, ADMIN)
- **Gestión de perfil propio**: Ver, editar y cambiar contraseña del usuario autenticado
- **RBAC**: Control de acceso basado en roles en endpoints existentes
- **Dependencias**: Se integra con BaseRepository, UnitOfWork, y dependencias de seguridad de `backend-patterns`

## Capabilities

### New Capabilities

- `user-registration`: Registro de usuarios con email/password, auto-asignación rol CLIENT
- `user-login`: Login con JWT (access + refresh tokens), rate limiting por IP
- `token-refresh`: Renovación de access token usando refresh token
- `user-logout`: Invalidación de refresh tokens
- `role-based-access`: Middleware de autorización por roles en endpoints
- `user-profile-management`: CRUD del perfil propio del usuario autenticado
- `password-change`: Cambio de contraseña con verificación de password actual

### Modified Capabilities

- No hay capacidades existentes que requieran modificación de requisitos — todas son nuevas.

## Impact

- **Backend**: Módulos `modules/auth/`, `modules/usuarios/`, `modules/refreshtokens/`
- **API**: 12+ endpoints nuevos bajo `/api/v1/auth/`, `/api/v1/usuarios/`, `/api/v1/perfil/`
- **Database**: Tablas `usuarios`, `refresh_tokens` (modelos por definir en modules)
- **Dependencias**: `backend-patterns` ✅ YA IMPLEMENTADO (BaseRepository, UoW, deps.py, security.py)