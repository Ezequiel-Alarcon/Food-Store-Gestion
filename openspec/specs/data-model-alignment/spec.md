# Spec: data-model-alignment

> **Tipo:** Alineación de modelo de datos con ERD v5  
> **Cambio padre:** `data-model-debt`

## Cambios

### CAMBIO-01: ProductoCategoria.es_principal
- **Modelo:** `productos/model.py` — `ProductoCategoria`
- **Nuevo campo:** `es_principal: bool = Field(default=False)`
- **Migración:** Agregar columna con default FALSE

### CAMBIO-02: ProductoIngrediente.es_removible
- **Modelo:** `productos/model.py` — `ProductoIngrediente`
- **Nuevo campo:** `es_removible: bool = Field(default=False)`
- **Migración:** Agregar columna con default FALSE

### CAMBIO-03: Categoria.eliminado_en
- **Modelo:** `categorias/model.py` — `Categoria`
- **Eliminar:** `activa: bool`
- **Nuevo campo:** `eliminado_en: Optional[datetime]`
- **Migración:** Agregar columna + migrar datos + eliminar columna vieja

### CAMBIO-04: Ingrediente.nombre unique
- **Modelo:** `ingredientes/model.py` — `Ingrediente`
- **Constraint:** `unique=True` en `nombre`
- **Migración:** Unique index parcial (WHERE eliminado_en IS NULL)
