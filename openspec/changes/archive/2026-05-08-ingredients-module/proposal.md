## Why

El módulo de ingredientes es esencial para el dominio de catálogo de Food Store. Permite registrar los componentes de cada producto, identificar alérgenos comunes (gluten, lactosa, frutos secos, maní), y cumplir con las regulaciones alimentarias. Sin este módulo, no es posible mostrar información de alérgenos a los clientes ni gestionar la personalización de pedidos (exclusión de ingredientes).

## What Changes

- **Nuevo módulo backend** `ingredientes/` con arquitectura Router → Service → UoW → Repository → Model
- **CRUD completo** de ingredientes: crear, listar, obtener, actualizar, soft-delete
- **Campo `es_alergeno`** boolean para marcar alérgenos comunes
- **Relación muchos-a-muchos** con productos (ProductoIngrediente)
- **Schemas Pydantic v2** separados (Create/Update/Read)
- **Migración Alembic** para la tabla `ingredientes`
- **Endpoints REST** bajo `/api/v1/ingredientes/`
- **Tests de unidad** cubriendo repository y service
- **Permisos RBAC**: ADMIN y STOCK pueden gestionar; CLIENT y PEDIDOS tienen acceso de lectura

## Capabilities

### New Capabilities
- `ingredient-crud`: Gestión completa de ingredientes con soft-delete
- `ingredient-allergen`: Flag booleano `es_alergeno` para identificación de alérgenos

### Modified Capabilities
- (ninguna — este es un módulo nuevo)

## Impact

**Backend:**
- `backend/app/modules/ingredientes/` nuevo directorio
- `backend/app/db/migrations/versions/` nueva migración
- Dependencias: hereda de `BaseRepository[T]`, `UnitOfWork`, `CategoriaRepository` existente

**Frontend:**
- `frontend/src/entities/ingrediente/` entidad + hooks
- `frontend/src/features/ingredients/` CRUD UI

**API:**
- `POST /api/v1/ingredientes/` — crear ingrediente
- `GET /api/v1/ingredientes/` — listar (paginación)
- `GET /api/v1/ingredientes/{id}` — obtener detalle
- `PATCH /api/v1/ingredientes/{id}` — actualizar parcialmente
- `DELETE /api/v1/ingredientes/{id}` — soft-delete

**Base de datos:**
- Tabla `ingredientes` con campos: id, nombre, descripcion, es_alergeno, creado_en, actualizado_en, eliminado_en
- Tabla intermedia `producto_ingrediente` (relación N:N)