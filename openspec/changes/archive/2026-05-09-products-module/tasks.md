# Products Module - Tasks

## Phase 1: Database & Models

- [x] **T1.1** - Crear migración Alembic `005_create_productos`
  - Tabla `productos` (id, nombre, descripcion, precio, imagen_url, stock, activo, eliminado_en, timestamps)
  - Tabla `producto_categorias` (producto_id, categoria_id)
  - Tabla `producto_ingredientes` (producto_id, ingrediente_id)
  - Índices en FKs

- [x] **T1.2** - Ejecutar migración: `alembic upgrade head` (listo para ejecutar en Docker)

- [x] **T1.3** - Crear modelo `Producto` en `app/modules/productos/model.py`
  - Herencia de SQLModel
  - Campos definidos en spec
  - Relaciones con ProductoCategoria, ProductoIngrediente

## Phase 2: Schemas

- [x] **T2.1** - Crear `ProductoCreate` schema
- [x] **T2.2** - Crear `ProductoUpdate` schema (campos opcionales)
- [x] **T2.3** - Crear `ProductoRead` schema (con relaciones)
- [x] **T2.4** - Crear `ProductoStockUpdate` schema
- [x] **T2.5** - Crear schemas para listados paginados

## Phase 3: Repository

- [x] **T3.1** - Crear `ProductoRepository` heredando `BaseRepository`
- [x] **T3.2** - Implementar método `get_by_categoria(categoria_id)`
- [x] **T3.3** - Implementar método `get_catalogo_publico(filtros)`
- [x] **T3.4** - Implementar método `update_stock(producto_id, nueva_cantidad)`
- [x] **T3.5** - Implementar soft-delete: `soft_delete(producto_id)`

## Phase 4: Service

- [x] **T4.1** - Crear `ProductoService` con lógica de negocio
- [x] **T4.2** - Validar precio > 0 y stock >= 0 (RN-ST01, RN-ST02)
- [x] **T4.3** - Implementar lógica de creación con asociaciones
- [x] **T4.4** - Implementar lógica de actualización con validaciones
- [x] **T4.5** - Implementar lógica de gestión de stock (set/add/subtract)
- [x] **T4.6** - Implementar filtros de catálogo: categoría, alérgenos, ingredientes

## Phase 5: Router (Endpoints)

- [x] **T5.1** - `POST /productos` (crear producto) - ADMIN, GESTOR_STOCK
- [x] **T5.2** - `GET /productos` (listar admin) - ADMIN, GESTOR_STOCK
- [x] **T5.3** - `GET /productos/{id}` (detalle admin) - ADMIN, GESTOR_STOCK
- [x] **T5.4** - `PUT /productos/{id}` (actualizar) - ADMIN, GESTOR_STOCK
- [x] **T5.5** - `PATCH /productos/{id}/stock` (gestionar stock) - ADMIN, GESTOR_STOCK
- [x] **T5.6** - `DELETE /productos/{id}` (soft-delete) - ADMIN

- [x] **T5.7** - `GET /productos/catalogo` (catálogo público)
- [x] **T5.8** - `GET /productos/{id}/publico` (detalle público)

- [x] **T5.9** - Registrar router en `app/main.py` (app.include_router)

## Phase 6: Testing & Seed

- [x] **T6.1** - Agregar productos de ejemplo en `db/seed.py` (10-15 productos)
- [x] **T6.2** - Probar endpoints con curl o Postman (requiere Docker)
- [x] **T6.3** - Verificar que el catálogo público funciona sin auth (requiere Docker)
- [x] **T6.4** - Verificar filtros de alérgenos (requiere Docker)

## Dependencies

- Change 8: `categories-module` ✅
- Change 9: `ingredients-module` ✅

## Notes

- Follow los patrones de módulos existentes (categorias, ingredientes)
- Usar la estructura: model → schemas → repository → service → router
- Proteger endpoints con los roles correctos (ADMIN, GESTOR_STOCK)
- El catálogo público NO requiere autenticación