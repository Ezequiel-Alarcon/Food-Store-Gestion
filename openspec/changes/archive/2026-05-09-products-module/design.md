## Context

El módulo de productos es el núcleo del e-commerce. Depende de los módulos de categorías (8) e ingredientes (9) ya implementados. Se necesita un CRUD completo con gestión de stock y un catálogo público con filtros por alérgenos.

## Goals / Non-Goals

**Goals:**
- Implementar CRUD completo de productos con soft-delete
- Gestionar relaciones muchos-a-muchos con categorías e ingredientes
- Implementar gestión de stock (incrementar/decrementar/set)
- Crear catálogo público sin auth con filtros por categoría y alérgenos
- Seguir los patrones existentes: BaseRepository, UoW, schemas Pydantic separados

**Non-Goals:**
- Frontend de productos (se implementa en change 18: cart-frontend)
- Integración con pedidos (change 13: orders-fsm)
- Dashboard de gestión de stock (change 12 solo backend)

## Decisions

### D1: Estructura de archivos del módulo

Siguiendo el patrón de módulos existentes (categorias, ingredientes):
```
backend/app/modules/productos/
├── __init__.py
├── model.py           # SQLModel: Producto, ProductoCategoria, ProductoIngrediente
├── schemas.py         # Pydantic: ProductoCreate, ProductoUpdate, ProductoRead
├── repository.py      # ProductoRepository (hereda BaseRepository)
├── service.py         # ProductoService
└── router.py          # FastAPI router con todos los endpoints
```

### D2: Esquemas Pydantic

Separación clara entre:
- `ProductoCreate`: campos para crear (sin id, sin timestamps)
- `ProductoUpdate`: campos para actualizar (todos opcionales)
- `ProductoRead`: respuesta completa (con id, timestamps, relaciones)
- `ProductoStockUpdate`: khusus para gestión de stock

### D3: Relaciones muchos-a-muchos

Usar tablas de join explícitas (no relationship() de SQLAlchemy):
- `producto_categorias`: producto_id + categoria_id
- `producto_ingredientes`: producto_id + ingrediente_id

Esto sigue el patrón usado en otros módulos y permite queries más eficientes.

### D4: Filtros de alérgenos en el catálogo público

La query del catálogo público filtra productos donde:
- `activo = true` AND `eliminado_en IS NULL`
- Si `excluir_alergenos=true`: NO existe en producto_ingredientes donde ingrediente.es_alergeno = true
- Si se pasan `ingrediente_ids`: NO existe en producto_ingredientes con esos IDs

Esto requiere un JOIN con la tabla de ingredientes.

### D5: Soft-delete

Campo `eliminado_en: datetime | None` en el modelo. Repository filtra automáticamente `eliminado_en IS NULL` en queries de lectura (salvo admin). Update/Soft-delete solo cambia este campo.

## Risks / Trade-offs

### R1: Race condition en stock

**Riesgo**: Dos gestores de stock modifican el mismo producto simultáneamente.
**Mitigación**: Usar `SELECT FOR UPDATE` en la transacción de UoW o implementar optimistic locking con versión.

### R2: Performance con muchos filtros

**Riesgo**: Filtros combinados (categoría + alérgenos) pueden lentizarse con mucho volumen.
**Mitigación**: Crear índices en las tablas de join. Considerar materialized views para el catálogo si el volumen crece.

### R3: Migration de base de datos

**Riesgo**: Agregar nuevas tablas y campos requiere migración.
**Mitigación**: Crear migración Alembic nueva (005) con las tablas producto, producto_categorias, producto_ingredientes.

## Migration Plan

1. Crear migración Alembic `005_create_productos`:
   - Tabla `productos` con todos los campos
   - Tabla `producto_categorias` (FK a productos y categorias)
   - Tabla `producto_ingredientes` (FK a productos e ingredientes)
   - Índices en FKs y en nombre

2. Aplicar migración: `alembic upgrade head`

3. Ejecutar seed.py para agregar productos de ejemplo (opcional)

4. Deploy: los nuevos endpoints están disponibles bajo `/api/v1/productos/`

## Open Questions

- **Q1**: ¿Cuántos productos de ejemplo necesitamos en el seed? → Decisión: 10-15 productos con distintas categorías
- **Q2**: ¿El catálogo debe paginar por cursor o por offset? → Decisión: offset (siguiente en change 18)
- **Q3**: ¿Proveemos imágenes de ejemplo? → Decisión: URLs placeholder de productos genéricos