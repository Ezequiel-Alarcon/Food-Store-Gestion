# Tasks: admin-catalog-ui

> **Objetivo:** Crear UI de gestión de catálogo (categorías + productos) para el panel admin y badges de alérgenos.  
> **Tiempo estimado:** 2-3 horas.  
> **Backend:** Sin cambios. Solo frontend.

---

## 1. Categorías CRUD — Admin

- [x] 1.1 Crear `features/admin/categories/CategoriesPage.tsx`
- [x] 1.2 Crear `CategoriesModal.tsx`
- [x] 1.3 `useMutation` para POST + PUT + invalidar query + toast.
- [x] 1.4 `useMutation` para DELETE con confirmación modal + toast.
- [x] 1.5 Crear `features/admin/categories/index.ts` barrel export.
- [x] 1.6 Agregar ruta `/admin/categorias` en `RouterProvider.tsx`
- [x] 1.7 Agregar link en `Navigation.tsx` para ADMIN.
- [x] 2.1 Crear `features/admin/products/ProductsPage.tsx`
- [x] 2.2 Crear `ProductFormModal.tsx`
- [x] 2.3 `useMutation` para POST + PUT + invalidar query + toast.
- [x] 2.4 `useMutation` para DELETE con confirmación modal + toast.
- [x] 2.5 Crear `features/admin/products/index.ts` barrel export.
- [x] 2.6 Agregar ruta `/admin/productos` en `RouterProvider.tsx`
- [x] 2.7 Agregar link en `Navigation.tsx` para ADMIN.
- [x] 3.1 `entities/producto/types.ts` — `es_alergeno: boolean` a `IngredienteSimple`.
- [x] 3.2 `IngredientsModal.tsx` — Badge ⚠️ ALÉRGENO.
- [x] 3.3 Rutas y navegación integradas.
- [x] 4.1-4.4 Verificación — componentes creados, rutas agregadas, tipos actualizados.
