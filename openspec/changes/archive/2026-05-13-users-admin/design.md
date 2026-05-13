## Context

El módulo `usuarios/` existe con router, service y repository pero `schemas.py` está vacío y no hay tests. El change busca completar la implementación siguiendo los patrones del proyecto.

## Goals / Non-Goals

**Goals:**
- Completar `schemas.py` con Pydantic v2 schemas (Create, Update, Read)
- Reforzar validation en router.py usando los schemas
- Agregar tests de integración covering los 4 endpoints

**Non-Goals:**
- No crear nuevos endpoints (los 4 existentes ya están definidos)
- No modificar el modelo `Usuario` (ya existe en `auth/model.py`)
- No agregar lógica de negocio nueva (service ya tiene la lógica)

## Decisions

### 1. Schema structure — seguir patrón Pydantic v2 del proyecto

**Decision:** Usar `BaseModel` con `model_config` en lugar de `Config` class.

**Rationale:** El proyecto usa Pydantic v2. Los módulos existentes (ej: `pedidos`, `pagos`) usan el patrón de schemas separados (`Create`, `Update`, `Read`) exportados desde `schemas.py`.

**Alternatives considered:**
- Usar un solo schema con campos opcionales → No, viola el principio de separated schemas del proyecto
- Usar `Config` class (Pydantic v1 style) → No, deprecated en v2

### 2. Response models en router.py

**Decision:** Mantener los dict returns actuales pero tiparlos con los nuevos response schemas.

**Rationale:** El router actualmente retorna `list[dict]` y `dict`. Cambiar a `response_model` explícito con schema tipado mejora la documentación OpenAPI sin cambiar el comportamiento.

### 3. Tests — seguir patrón de tests de módulos existentes

**Decision:** Crear `backend/tests/modules/usuarios/test_usuarios_endpoints.py` con fixtures similares a `test_pedidos_endpoints.py`.

**Rationale:** Ya existe un patrón de tests de integración en el proyecto. Seguirlo garantiza consistencia.

**Alternatives considered:**
- Tests unitarios → No, el proyecto prioriza tests de integración
- Tests de事务所 (mock) → No, preferimos tests con DB real via override_get_session

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| `schemas.py` vacío desde el inicio — esqueloto sin uso real | Seguir el patrón exacto de `schemas.py` de módulos funcionales (ej: `pedidos/schemas.py`) |
| Los endpoints no respondan con los schemas esperados | Verificar con tests de integración |

## Open Questions

Ninguna — el scope está definido y los endpoints ya existen.