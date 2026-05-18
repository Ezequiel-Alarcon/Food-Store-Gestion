# Tasks: data-model-debt

> **Objetivo:** Alinear 4 campos del modelo de datos con ERD v5.  
> **Backend only.** Requiere migración Alembic.

## 1. ProductoCategoria + es_principal

- [x] 1.1 `productos/model.py` — `es_principal: bool = Field(default=False)`
- [x] 1.2 `productos/schemas.py` — campo en schema
- [x] 1.3 Migración: `es_principal` agregado
- [x] 2.1 `productos/model.py` — `es_removible: bool = Field(default=False)`
- [x] 2.2 `productos/schemas.py` — campo en schema
- [x] 2.3 Migración: `es_removible` agregado
- [x] 3.1 `categorias/model.py` — `activa` → `eliminado_en`
- [x] 3.2 `categorias/repository.py` — queries actualizadas
- [x] 3.3 `categorias/service.py` — soft-delete con timestamp
- [x] 3.4 Migración: columna + datos + drop
- [x] 4.1 `ingredientes/model.py` — `unique=True`
- [x] 4.2 `ingredientes/service.py` — validación duplicados
- [x] 4.3 Migración: unique index parcial
- [x] 5.1-5.4 Verificación + archive + engram sync + commit + push
