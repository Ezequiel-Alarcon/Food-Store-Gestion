## 1. Entidad Producto (API client)

- [x] 1.1 Crear `entities/producto/types.ts` — interfaces: `ProductoCatalogo`, `ProductoDetalle`, `ProductoCatalogoResponse` (con page/size/total)
- [x] 1.2 Crear `entities/producto/api.ts` — funciones: `getProductos(params)` con filtros (categoria, disponible, search, page, size) y `getProductoById(id)`
- [x] 1.3 Crear `entities/producto/index.ts` — barrel export

## 2. Página de Catálogo (`/productos`)

- [x] 2.1 Crear `pages/CatalogPage.tsx` — grid responsive de productos con fetch desde `getProductos()`, estado loading/error/empty, paginación
- [x] 2.2 Crear `features/cart/ProductCard.tsx` — tarjeta de producto con imagen, nombre, precio, stock, botón "Agregar"
- [x] 2.3 Crear `features/cart/IngredientsModal.tsx` — modal con checkboxes de ingredientes para exclusión (US-030)
- [x] 2.4 Agregar ruta `/productos` en `providers/RouterProvider.tsx`

## 3. Cart Drawer + Cart Summary

- [x] 3.1 Crear `features/cart/CartDrawer.tsx` — panel lateral derecho con overlay, animación slide, conectado a `uiStore.cartOpen`
- [x] 3.2 Crear `features/cart/CartSummary.tsx` — lista de items con nombre, cantidad, precio unitario, exclusiones, subtotal, total, botón eliminar, botón vaciar carrito
- [x] 3.3 Agregar ruta `/carrito` en `providers/RouterProvider.tsx` (página dedicada opcional, reutiliza CartSummary)

## 4. Integración en navegación

- [x] 4.1 Agregar badge con contador de items en el ícono del carrito en `features/layout/Navigation.tsx`
- [x] 4.2 Conectar clic del ícono a `uiStore.toggleCart()` para abrir/cerrar el drawer

## 5. Verificación

- [x] 5.1 Probar flujo completo: navegar a `/productos` → agregar producto → abrir drawer → modificar cantidad → eliminar item → vaciar carrito
- [x] 5.2 Probar exclusión de ingredientes: producto con ingredientes → abrir modal → desmarcar ingredientes → confirmar → verificar en drawer
- [x] 5.3 Verificar persistencia: agregar items → refrescar página → verificar que el carrito mantiene los items
