# Proposal: post-audit-fixes

## Why

La re-auditoría post-cambios encontró 4 bugs críticos que crashean la app: 3 referencias a `Categoria.activa` (columna dropeada por `data-model-debt`) en backend, y `CheckoutPage` con `addToast`/`clearCart` undefined (regresión de `mvp-critical-fixes`). También hay 2 issues altos: schemas faltantes y query key collision.

## What Changes

- **B1-B3:** Reemplazar 10 referencias a `Categoria.activa` por `Categoria.eliminado_en is None` en `productos/service.py`, `categorias/router.py`, `seed.py`.
- **N1:** Agregar `addToast` y `clearCart` al destructuring en `CheckoutPage.tsx`.
- **B4:** Agregar `es_principal` a `CategoriaSimple` y `es_removible` a `IngredienteSimple` en schemas.
- **N2:** Cambiar query key de StockManagementPage a `['admin-productos-stock']`.

## Impact

- **Archivos:** 5 backend + 2 frontend
- **Riesgo:** Bajo — fixes puntuales, sin cambios de arquitectura
