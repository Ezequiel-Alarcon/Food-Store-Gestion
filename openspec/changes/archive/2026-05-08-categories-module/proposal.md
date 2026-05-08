## Why

El módulo de categorías es la base del catálogo de productos. Sin él, los productos no pueden organizarse jerárquicamente (ej: Comidas → Italiana → Pizzas). Se necesita CRUD completo con estructura recursiva para navegación del menú y filtrado.

## What Changes

- Nuevo módulo `backend/app/modules/categorias/` con arquitectura estándar (modelo, schemas, repository, service, router)
- Endpoint público `/api/v1/categorias/` — listado jerárquico con CTE recursiva
- CRUD completo con soft-delete (nunca se borra físicamente)
- Endpoint `/api/v1/categorias/arbol` para返回 árbol completo con hijos anidados
- Endpoint `/api/v1/categorias/{id}/subcategorias` para obtener descendientes
- Validación de ciclos: no permitir que una categoría sea hija de sí misma ni de sus descendientes

## Capabilities

### New Capabilities

- `category-crud`: CRUD completo de categorías con soft-delete. Crear, listar, editar, eliminar. Validación de nombres únicos por nivel.
- `category-hierarchy`: Estructura jerárquica padre-hijo. Listado recursivo con CTE. Obtención de ancestors y descendants.

### Modified Capabilities

- _(ninguna — es módulo nuevo)_

## Impact

- **Backend**: Nuevo módulo `categorias/` siguiendo patrón feature-first
- **Dependencias**: `auth-backend` (ya archivado) — requiere `get_current_user` para endpoints protegidos
- **Impacto en productos**: productos-module (change 10) depende de este módulo para asociar categorías
- **API pública**: `/api/v1/categorias/` será consumida por frontend para navegación del menú
