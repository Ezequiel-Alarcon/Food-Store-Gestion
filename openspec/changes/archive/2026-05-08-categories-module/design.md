## Context

Módulo de gestión de categorías jerárquicas para el catálogo de productos de Food Store. Las categorías forman un árbol donde cada categoría puede tener un padre (excepto raíces) y múltiples hijos. Ejemplo: Comidas → Italiana → Pizzas.

## Goals / Non-Goals

**Goals:**
- CRUD completo de categorías con soft-delete (eliminación lógica)
- Estructura jerárquica padre-hijo usando Adjacency List (parent_id)
- Listado recursivo del árbol completo usando CTE de PostgreSQL
- Obtención de ancestors y descendants de cualquier categoría
- Validación de ciclos: no permitir que una categoría sea hija de sí misma ni de sus descendientes
- Validación de nombres únicos por nivel (hermanos no pueden tener mismo nombre)

**Non-Goals:**
- No implementar Closure Table (complejidad innecesaria para este caso de uso)
- No implementar migración de categorías existentes (no hay datos aún)
- No implementar categorización multi-padre (una categoría tiene un solo padre)

## Decisions

### 1. Adjacency List en lugar de Closure Table

**Decisión:** Usar `parent_id` (NULL para raíces) + CTE recursiva para queries jerárquicas.

**Alternativas consideradas:**
- **Closure Table**: Tabla separada con todos los pares ancestor-descendant. Más rápido para queries pero requiere mantener sincronía. Overkill para este caso.
- **Nested Sets**: Muy rápido para lecturas, lento para writes. No soportado nativamente por PostgreSQL.

**Rationale:** PostgreSQL soporta CTEs recursivas nativas. La complejidad es mínima y el modelo es intuitivo. Las queries recursivas son performantes con índices en `parent_id`.

### 2. Modelo SQLModel con Soft-Delete

**Decisión:** Campo `activa: bool = True` en lugar de `deleted_at`.

**Rationale:** Simple de consultar (WHERE activa = true). Más fácil de re-activar si se necesita. El timestamp es innecesario para el caso de uso.

### 3. Validación de ciclos en Service Layer

**Decisión:** Validar antes de insertar/actualizar `parent_id` consultando si el nuevo padre es descendant de la categoría.

**Alternativas:**
- **Trigger de DB**: Funciona pero oculta la lógica de negocio.
- **CTE en UPDATE**: Más complejo, menos legible.

**Rationale:** La validación en service layer es clara, testeable, y mantiene la lógica de dominio cerca del código.

## Decisions

### 4. Campos del Modelo Categoria

```
- id: int (PK, auto)
- nombre: str (max 100, unique por nivel)
- slug: str (auto-generado, unique)
- descripcion: str | None (opcional)
- padre_id: int | None (FK self, NULL = raíz)
- orden: int (para sorting manual)
- activa: bool (soft-delete flag)
- created_at: datetime
- updated_at: datetime
```

**Rationale:**
- `orden` permite sorting manual (drag & drop futuro) además de alphabetical
- `slug` para URLs amigables (/categorias/pizzas)
- `descripcion` para SEO y mostrar en UI

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| CTE recursiva性能 en árboles muy profundos (>100 niveles) | Agregar `MAX_RECURSION` de 50 niveles, validar profundidad máxima |
| Nombres únicos por nivel vs global uniqueness | Validar uniqueness solo entre siblings (`padre_id` igual) |
| Cambiar padre_id de categoría con hijos | Los hijos mantienen su关联, el árbol se re-estructura |

## Migration Plan

1. Crear migración Alembic `add_categorias_table`
2. Registrar router en `main.py`
3. Tests de integración
4. Sin impacto en datos (tabla nueva)
