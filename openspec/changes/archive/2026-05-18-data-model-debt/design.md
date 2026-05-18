# Design: data-model-debt

## Context

El ERD v5 define campos que el código actual no implementa. Son 4 fixes de modelo con migración Alembic. Cambios pequeños y localizados.

## Goals / Non-Goals

**Goals:**
- Agregar `es_principal` a ProductoCategoria
- Agregar `es_removible` a ProductoIngrediente
- Migrar Categoria de `activa: bool` a `eliminado_en: datetime`
- Agregar `unique=True` a Ingrediente.nombre

**Non-Goals:**
- NO modificar endpoints
- NO cambiar schemas de response (solo agregar campos nuevos donde aplique)

## Decisions

### Fix 1: ProductoCategoria.es_principal
- **Modelo:** `es_principal: bool = Field(default=False)`
- **Migración:** `ALTER TABLE productos_categorias ADD COLUMN es_principal BOOLEAN DEFAULT FALSE`
- **Schema:** Agregar al response de producto (opcional, default false)
- **Impacto:** Ninguno en endpoints existentes. Campo nuevo con default.

### Fix 2: ProductoIngrediente.es_removible
- **Modelo:** `es_removible: bool = Field(default=False)`
- **Migración:** `ALTER TABLE productos_ingredientes ADD COLUMN es_removible BOOLEAN DEFAULT FALSE`
- **Schema:** Agregar al response de producto-ingrediente
- **Impacto:** Habilita personalización de pedidos. El frontend ya tiene el tipo actualizado (allergen-badges-ui).

### Fix 3: Categoria.eliminado_en
- **Modelo:** Reemplazar `activa: bool` por `eliminado_en: Optional[datetime]`
- **Migración:** `ALTER TABLE categorias ADD COLUMN eliminado_en TIMESTAMPTZ; UPDATE categorias SET eliminado_en = NOW() WHERE activa = false; ALTER TABLE categorias DROP COLUMN activa`
- **Service:** Actualizar queries que usaban `activa` → usar `eliminado_en IS NULL`
- **Impacto:** Rompe queries que filtran por `activa`. Requiere actualizar repository y service.

### Fix 4: Ingrediente.nombre unique
- **Modelo:** Agregar `unique=True` (índice único en BD) o `sa_column=Column(String(100), unique=True)`
- **Service:** Agregar validación en create/update para nombre duplicado
- **Migración:** `CREATE UNIQUE INDEX ON ingredientes (nombre) WHERE eliminado_en IS NULL`
- **Impacto:** Puede fallar si ya hay duplicados en BD. Verificar antes.

## Risks / Trade-offs

- **[Riesgo] Fix 3: Migración de activa→eliminado_en.** Datos existentes: si hay categorías con `activa=false`, se les asigna `eliminado_en=NOW()`. → **Mitigación:** Backup mental, es entorno dev.
- **[Riesgo] Fix 4: Unique constraint.** Si hay ingredientes duplicados en BD, la migración falla. → **Mitigación:** Usar índice parcial `WHERE eliminado_en IS NULL` para solo forzar unique en activos.
