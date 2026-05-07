## 1. Core persistence patterns

- [x] 1.1 Implementar `UnitOfWork` como context manager en `backend/app/core/uow.py` (commit/rollback)
- [x] 1.2 Implementar factory de sesión por-request (si aplica) y wiring mínimo en `backend/app/core/database.py`
- [x] 1.3 Implementar `BaseRepository[T]` en `backend/app/core/repository.py` con operaciones CRUD básicas

## 2. Auth/RBAC dependencies

- [x] 2.1 Implementar `get_current_user` en `backend/app/core/deps.py` (resolver usuario desde JWT)
- [x] 2.2 Implementar `require_role(*roles)` en `backend/app/core/deps.py` (enforce RBAC)

## 3. Uso y verificación mínima

- [x] 3.1 Agregar un ejemplo mínimo (router/service) que demuestre UoW + BaseRepository + deps (commit vs rollback)
- [x] 3.2 Documentar brevemente el patrón de uso esperado (comentarios/docstrings) para que futuros módulos lo repliquen
