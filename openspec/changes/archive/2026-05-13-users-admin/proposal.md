## Why

El módulo `usuarios/` (CRUD administrativo de usuarios) fue creado en una sesión anterior pero quedó incompleto: `schemas.py` está vacío, no tiene validation schemas, y carece de tests de integración. Esto impide que el change sea mergeable y funcional para el equipo de frontend.

## What Changes

1. **Completar `schemas.py`** con schemas Pydantic para validation de requests/responses (Create, Update, Read)
2. **Reforzar validation en `router.py`** usando los nuevos schemas en lugar de `Query()` sueltas
3. **Agregar tests de integración** en `backend/tests/modules/usuarios/` (9 endpoints funcionales)
4. **Validar que los endpoints respondan correctamente** con el pipeline auth existente

## Capabilities

### New Capabilities
- `user-management`: Gestión administrativa de usuarios (listar, ver, actualizar, desactivar). Cada operación devuelve response models tipados.

### Modified Capabilities
- (ninguno — no cambia comportamiento existente, solo completa implementación)

## Impact

- **Code:** `backend/app/modules/usuarios/schemas.py` (nuevo), `backend/app/modules/usuarios/router.py` (refuerza validation)
- **Tests:** `backend/tests/modules/usuarios/` (nuevo directorio)
- **Dependencies:** Depende de `auth-backend` (change 6) — el modelo `Usuario` y `require_role` ya existen