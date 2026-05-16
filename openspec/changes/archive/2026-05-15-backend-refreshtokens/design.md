## Context

El módulo `refreshtokens` fue scaffolded durante la Fase 0-1 pero nunca completado. Actualmente:
- `model.py` y `repository.py` están completos y funcionales
- `service.py` existe pero opera sin Unit of Work (anti-patrón en este proyecto)
- `router.py` y `schemas.py` están vacíos
- El módulo NO está registrado en `main.py`
- No tiene tests dedicados

El flujo de refresh actual funciona a través de `auth/service.py` (que importa `RefreshTokenRepository` directamente), pero esto no expone endpoints administrativos para gestionar tokens (listar, revocar, auditar).

## Goals / Non-Goals

**Goals:**
- Completar el módulo `refreshtokens` como componente standalone con router, schemas y service funcionales
- Exponer endpoints admin-only para gestión de refresh tokens (listar por usuario, revocar individual, revocar todos)
- Refactorizar `service.py` para usar Unit of Work (consistencia con la arquitectura del proyecto)
- Agregar tests de integración para el módulo
- Registrar el módulo en `main.py`

**Non-Goals:**
- NO mover lógica de `auth/service.py` a `refreshtokens` — eso sería un refactor mayor fuera de scope
- NO agregar campo `family_id` al modelo — requiere nueva migración y cambios en auth
- NO cambiar el flujo de refresh actual (`/auth/refresh`) — sigue operando desde auth
- NO cambios en el frontend — ya funciona correctamente

## Decisions

### 1. Endpoints admin-only (RBAC: admin)
Los endpoints de gestión de refresh tokens requieren rol `admin`. Esto protege operaciones sensibles como revocar tokens de otros usuarios. Se usa `require_role("admin")` de `core/deps.py`.

**Alternativa considerada**: Permitir que cada usuario gestione solo sus propios tokens. Se descarta porque el caso de uso principal es administrativo (soporte, auditoría, forced logout).

### 2. Service usa Unit of Work
`RefreshTokenService` se refactoriza para recibir `UnitOfWork` en lugar de `Session` directa. Cada operación envuelve la transacción en `with uow:` para commit automático o rollback en error.

**Alternativa considerada**: Mantener el patrón actual (session directa). Se descarta porque viola la convención del proyecto y rompe la atomicidad transaccional.

### 3. Schemas Pydantic v2 con ConfigDict
Los schemas usan `model_config = ConfigDict(from_attributes=True)` en lugar de `class Config:`. Siguen la convención del proyecto para Pydantic v2.

### 4. Sin migración nueva para el índice
El índice en la columna `token` se agrega modificando `model.py` directamente (SQLModel soporta `index=True`). Si la tabla ya existe, se genera una migración alembic simple con `CREATE INDEX`.

### 5. Respuestas con formato snake_case
Los schemas de respuesta usan snake_case (`user_id`, `expires_at`, `revocado`) para alinearse con el resto de la API y el frontend.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| `auth/service.py` sigue importando `RefreshTokenRepository` directamente (no el service) | Fuera de scope — se documenta como deuda técnica para futuro refactor |
| Agregar índice en tabla existente requiere migración manual | Se genera migración alembic con `op.create_index()` |
| Endpoints nuevos no están cubiertos por tests existentes | Se crean tests dedicados en `tests/modules/refreshtokens/` |
| `PerfilService` también importa `RefreshTokenRepository` directamente | Mismo caso que auth — fuera de scope, se documenta |
