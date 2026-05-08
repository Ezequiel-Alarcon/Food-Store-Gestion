## Context

El módulo de ingredientes es parte del dominio de catálogo de Food Store. Según la descripción del sistema, un **Ingrediente** registra los componentes de cada producto, con un campo booleano `es_alergeno` para identificar alérgenos comunes. La relación entre productos e ingredientes es muchos-a-muchos (tabla `producto_ingrediente`).

Este módulo hereda la arquitectura Router → Service → UoW → Repository → Model usada en el módulo `categorias`. La estructura de archivos será similar, adaptando los patrones establecidos.

## Goals / Non-Goals

**Goals:**
- CRUD completo de ingredientes con soft-delete
- Flag `es_alergeno` para identificar alérgenos comunes
- Permisos RBAC diferenciados: ADMIN/STOCK escriben, todos los roles leen
- Tests de unidad cubriendo repository y service

**Non-Goals:**
- Gestión de la relación producto-ingrediente (eso es parte del módulo productos)
- Frontend UI completo — solo entidad y hooks básicos
- Algoritmos de sugerencia de alérgenos o validación automática

## Decisions

### 1. Arquitectura de archivos (igual a categorias)

Decisión: seguir la misma estructura de `categorias/` para ingredientes.

```
backend/app/modules/ingredientes/
├── __init__.py
├── model.py      # SQLModel Ingrediente
├── schemas.py    # Pydantic Create/Update/Read
├── repository.py # IngredienteRepository(BaseRepository)
├── service.py    # IngredienteService
└── router.py     # API endpoints
```

**Rationale**: Consistencia entre módulos feature-first. El equipo sabe dónde buscar cada cosa.

### 2. Modelo Ingrediente

```python
from datetime import datetime, timezone

class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    descripcion: str | None = Field(default=None, max_length=500)
    es_alergeno: bool = Field(default=False)
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actualizado_en: datetime | None = Field(default=None)
    eliminado_en: datetime | None = Field(default=None)  # soft delete
```

**Rationale**: `es_alergeno` default `False` porque la mayoría de ingredientes no son alérgenos. Soft-delete incluido por consistencia con el resto del sistema. Se usa `datetime.now(timezone.utc)` en lugar del deprecated `datetime.utcnow()`.

### 3. Nomenclatura de endpoints

- `POST /api/v1/ingredientes/` — crear
- `GET /api/v1/ingredientes/` — listar (paginación con skip/limit)
- `GET /api/v1/ingredientes/{id}` — obtener uno
- `PATCH /api/v1/ingredientes/{id}` — actualizar parcialmente
- `DELETE /api/v1/ingredientes/{id}` — soft-delete

**Rationale**: Coherencia con la convención REST del proyecto. El prefijo `api/v1/` ya está definido en el main.py.

### 4. Permisos RBAC

| Método | Roles |
|--------|-------|
| GET (list, get) | ADMIN, STOCK, PEDIDOS, CLIENT |
| POST, PATCH, DELETE | ADMIN, STOCK |

**Rationale**: CLIENT y PEDIDOS pueden leer ingredientes (para ver alérgenos en productos), pero solo ADMIN y STOCK pueden modificarlos.

### 5. Validación de nombre

- `nombre`: obligatorio, 1-100 caracteres, único entre ingredientes no eliminados
- `descripcion`: opcional, max 500 caracteres
- `es_alergeno`: boolean, default False

**Rationale**: El nombre único evita duplicados. Descripción opcional porque algunos ingredientes son muy simples (sal, pimienta).

## Risks / Trade-offs

[Risk] Nombre de ingrediente muy largo → Mitigation: limitar a 100 chars en Pydantic y DB
[Risk] Alérgenos cruzados (traza de maní en producto que dice "sin maní") → Mitigation: esto se maneja a nivel de producto, no aquí. El flag solo indica que el ingrediente ES un alérgeno conocido, no el contexto de uso.

## Migration Plan

1. Crear migración Alembic `002_add_ingredientes.py`
2. Aplicar migración: `alembic upgrade head`
3. Deploy código del módulo
4. Verificar que los endpoints respondan correctamente

Rollback: `alembic downgrade -1` revierte la migración.

## Open Questions

- ¿La tabla `producto_ingrediente` ya existe o se crea con este change?
  → Según Descripcion.txt, la tabla existe como parte del modelo de datos. La migración solo crea `ingredientes`, no la relación N:N.