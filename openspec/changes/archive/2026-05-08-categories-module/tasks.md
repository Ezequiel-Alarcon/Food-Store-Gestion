## 1. Model & Migration

- [x] 1.1 Create `backend/app/modules/categorias/model.py` with SQLModel `Categoria` (id, nombre, slug, descripcion, padre_id, orden, activa, created_at, updated_at)
- [x] 1.2 Create Alembic migration `add_categorias_table` with unique constraint on (nombre, padre_id) when activa=true
- [x] 1.3 Add self-referential FK constraint on padre_id
- [x] 1.4 Add index on padre_id and activa for query performance
- [x] 1.5 Run migration and verify table creation

## 2. Schemas (Pydantic v2)

- [x] 2.1 Create `backend/app/modules/categorias/schemas.py`
- [x] 2.2 `CategoriaCreate` schema (nombre, descripcion, padre_id, orden)
- [x] 2.3 `CategoriaUpdate` schema (nombre, descripcion, padre_id, orden)
- [x] 2.4 `CategoriaRead` schema (all fields including timestamps)
- [x] 2.5 `CategoriaTreeNode` schema with `hijos: list[CategoriaTreeNode]` for nested response

## 3. Repository

- [x] 3.1 Create `backend/app/modules/categorias/repository.py`
- [x] 3.2 Extend BaseRepository with soft-delete awareness (where `activa = true` default)
- [x] 3.3 Add `get_by_slug(slug)` method
- [x] 3.4 Add `get_children(parent_id)` method
- [x] 3.5 Add `get_descendants_cte(category_id, max_depth)` using PostgreSQL recursive CTE
- [x] 3.6 Add `check_cycle(category_id, new_parent_id)` for cycle detection
- [x] 3.7 Add `soft_delete_with_descendants(category_id)` to cascade soft-delete
- [x] 3.8 Add `get_siblings(parent_id, exclude_id)` for uniqueness check

## 4. Service

- [x] 4.1 Create `backend/app/modules/categorias/service.py`
- [x] 4.2 `create(data)` - validate uniqueness, auto-generate slug, create with UoW
- [x] 4.3 `get_by_id(id)` - return category or raise NotFound
- [x] 4.4 `list_all()` - return active categories ordered by orden, nombre
- [x] 4.5 `update(id, data)` - validate cycle, uniqueness, update with UoW
- [x] 4.6 `soft_delete(id)` - cascade to descendants
- [x] 4.7 `get_tree()` - build nested tree from flat list using CTE results
- [x] 4.8 `get_subcategorias(id, profundidad)` - return descendants up to depth

## 5. Router (API Endpoints)

- [x] 5.1 Create `backend/app/modules/categorias/router.py`
- [x] 5.2 `POST /api/v1/categorias/` - create category (ADMIN only)
- [x] 5.3 `GET /api/v1/categorias/` - list all active (authenticated)
- [x] 5.4 `GET /api/v1/categorias/{id}` - get single (authenticated)
- [x] 5.5 `PUT /api/v1/categorias/{id}` - update (ADMIN only)
- [x] 5.6 `DELETE /api/v1/categorias/{id}` - soft-delete cascade (ADMIN only)
- [x] 5.7 `GET /api/v1/categorias/arbol` - get full tree (authenticated)
- [x] 5.8 `GET /api/v1/categorias/{id}/subcategorias` - get descendants (authenticated)
- [x] 5.9 `GET /api/v1/categorias/publico/arbol` - public tree (no auth, rate limited)
- [x] 5.10 Register router in `backend/app/main.py`

## 6. Tests

- [x] 6.1 Create `backend/tests/modules/categorias/test_crud.py`
- [x] 6.2 Test create root category
- [x] 6.3 Test create child category
- [x] 6.4 Test duplicate name at same level (409)
- [x] 6.5 Test invalid parent (404)
- [x] 6.6 Test list all active categories
- [x] 6.7 Test get single category
- [x] 6.8 Test update category
- [x] 6.9 Test soft delete
- [x] 6.10 Test soft delete cascade
- [x] 6.11 Create `backend/tests/modules/categorias/test_hierarchy.py`
- [x] 6.12 Test get full tree structure
- [x] 6.13 Test empty tree
- [x] 6.14 Test get subcategorias with depth
- [x] 6.15 Test cycle prevention (self-parent)
- [x] 6.16 Test cycle prevention (descendant as parent)
- [x] 6.17 Test move category to different branch

## 7. Specs Sincronización

- [x] 7.1 Copy `specs/category-crud/spec.md` to `openspec/specs/category-crud/spec.md`
- [x] 7.2 Copy `specs/category-hierarchy/spec.md` to `openspec/specs/category-hierarchy/spec.md`