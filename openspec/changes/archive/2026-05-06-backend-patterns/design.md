## Context

El roadmap del proyecto define el backend con arquitectura en capas: **Router → Service → UoW → Repository → Model**. Hoy no hay un contrato explícito (ni helpers) para transacciones, repositorios genéricos ni dependencias de RBAC, lo que genera riesgo de:

- commits parciales (operaciones no atómicas)
- duplicación de CRUD/queries en cada módulo
- inconsistencias en autorización (cada router implementa “a su manera”)

Este change introduce patrones cross-cutting en `backend/app/core/` para que todos los módulos futuros los reutilicen.

## Goals / Non-Goals

**Goals:**
- Definir un **Unit of Work** como context manager para encapsular transacciones y asegurar **commit/rollback** consistente.
- Definir un **BaseRepository[T]** tipado para centralizar operaciones comunes y reducir boilerplate.
- Definir dependencias FastAPI para **autenticación y RBAC**: `get_current_user` y `require_role`.
- Establecer el wiring base para que el camino recomendado sea Router → Service → UoW → Repository.

**Non-Goals:**
- Implementar módulos de dominio (auth, productos, pedidos, etc.).
- Definir reglas de negocio específicas (eso se hace en changes por módulo).
- Optimización avanzada de queries o patrones DDD (spec/repo genérico y UoW básico alcanzan).

## Decisions

1) **UoW como context manager**
- **Decisión**: Implementar `UnitOfWork` con `__enter__/__exit__` para manejar `commit()` y `rollback()`.
- **Rationale**: Simplifica el uso en Services y garantiza rollback ante excepciones sin repetir try/except.
- **Alternativas**:
  - Decorator transaccional por endpoint: oculta control, más difícil de testear y de componer.
  - Manejo manual de sesión en cada service: propenso a errores y duplicación.

2) **BaseRepository genérico tipado**
- **Decisión**: `BaseRepository[T]` parametrizable por modelo (SQLModel/ORM) con operaciones comunes (get_by_id, list, create, update, soft_delete si aplica en cada módulo).
- **Rationale**: Reduce código repetido y estandariza acceso a datos.
- **Alternativas**:
  - Repositorio por entidad sin base: más explícito, pero genera boilerplate y divergencias.

3) **RBAC vía dependencias FastAPI**
- **Decisión**: `get_current_user` resuelve el usuario autenticado desde JWT; `require_role(*roles)` compone autorización.
- **Rationale**: Asegura un patrón uniforme y reutilizable en routers.
- **Alternativas**:
  - Checks dentro de services: acopla autorización al caso de uso; menos declarativo en routers.
  - Middleware global por path: rígido y difícil de expresar reglas por endpoint.

## Risks / Trade-offs

- **[Riesgo]** Un BaseRepository demasiado genérico puede tapar necesidades específicas → **Mitigación**: permitir repos por módulo que extiendan BaseRepository y agreguen queries propias.
- **[Riesgo]** Acoplamiento a la implementación de sesión/ORM → **Mitigación**: exponer la sesión a través del UoW y minimizar helpers “mágicos”.
- **[Trade-off]** Patrón UoW impone disciplina (usar siempre UoW) → Beneficio: atomicidad y consistencia transaccional.
