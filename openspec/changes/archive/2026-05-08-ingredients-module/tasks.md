## 1. Backend Setup

- [x] 1.1 Create module directory `backend/app/modules/ingredientes/`
- [x] 1.2 Create `__init__.py` files for Python package
- [x] 1.3 Register ingredient router in `backend/app/main.py`

## 2. Database Migration

- [x] 2.1 Create Alembic migration `003_add_ingredientes.py`
- [x] 2.2 Define table schema: id, nombre, descripcion, es_alergeno, creado_en, actualizado_en, eliminado_en
- [ ] 2.3 Test migration applies cleanly

## 3. Model Layer

- [x] 3.1 Create `model.py` with SQLModel Ingrediente class
- [x] 3.2 Add `__tablename__ = "ingredientes"`
- [x] 3.3 Include soft-delete field `eliminado_en`

## 4. Schemas Layer (Pydantic)

- [x] 4.1 Create `schemas.py`
- [x] 4.2 Define `IngredienteCreate` (nombre required, descripcion optional, es_alergeno default false)
- [x] 4.3 Define `IngredienteUpdate` (all fields optional)
- [x] 4.4 Define `IngredienteRead` (all fields including id, timestamps)
- [x] 4.5 Add validation: nombre max 100 chars, descripcion max 500 chars

## 5. Repository Layer

- [x] 5.1 Create `repository.py`
- [x] 5.2 Extend `BaseRepository[Ingrediente]`
- [x] 5.3 Add `get_by_nombre(nombre)` for duplicate checking
- [x] 5.4 Add `list_all(skip, limit, es_alergeno)` with optional filter
- [x] 5.5 Ensure soft-delete filtering in all queries

## 6. Service Layer

- [x] 6.1 Create `service.py`
- [x] 6.2 Implement `create(data: IngredienteCreate)` with duplicate name check
- [x] 6.3 Implement `list(skip, limit, es_alergeno)` passthrough to repository
- [x] 6.4 Implement `get_by_id(id)` passthrough to repository
- [x] 6.5 Implement `update(id, data: IngredienteUpdate)` with partial update support
- [x] 6.6 Implement `soft_delete(id)` using repository

## 7. Router Layer

- [x] 7.1 Create `router.py` with FastAPI APIRouter
- [x] 7.2 Add `POST /` with ADMIN/STOCK roles only, returns 201
- [x] 7.3 Add `GET /` with pagination (skip, limit), filter `es_alergeno`, all roles
- [x] 7.4 Add `GET /{id}` with all roles, returns 200 or 404
- [x] 7.5 Add `PATCH /{id}` with ADMIN/STOCK roles, returns 200 or 404
- [x] 7.6 Add `DELETE /{id}` with ADMIN/STOCK roles, returns 204 or 404
- [x] 7.7 Use `get_session` dependency injection for all endpoints

## 8. Tests

- [ ] 8.1 Create `tests/test_ingrediente_repository.py`
- [ ] 8.2 Test create ingredient
- [ ] 8.3 Test duplicate name detection
- [ ] 8.4 Test list with pagination
- [ ] 8.5 Test list filter by allergen
- [ ] 8.6 Test soft-delete
- [ ] 8.7 Create `tests/test_ingrediente_service.py`
- [ ] 8.8 Test create with validation
- [ ] 8.9 Test update partial
- [ ] 8.10 Test get_by_id not found

## 9. Frontend Entity

- [x] 9.1 Create `frontend/src/entities/ingrediente/` directory
- [x] 9.2 Define TypeScript types matching IngredienteRead
- [x] 9.3 Create API client functions (getAll, getById, create, update, delete)
- [x] 9.4 Export types and client for use by features

## 10. Spec File

- [x] 10.1 Create `openspec/specs/ingredient-crud/spec.md` with full requirements
- [x] 10.2 Reference all scenarios from tasks.md verification