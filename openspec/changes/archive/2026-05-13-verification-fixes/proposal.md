## Why

El backend de productos (`products-module`) está completo y archivado. El `cartStore` de Zustand ya está implementado con todas las acciones del carrito (agregar, modificar cantidad, eliminar, vaciar, persistencia en localStorage). Lo que falta es la capa de presentación frontend: los componentes que el usuario ve e interactúa — el catálogo de productos, el drawer del carrito y la integración de navegación. Sin esto, el cliente no puede agregar productos al carrito ni visualizar su pedido antes del checkout.

## What Changes

- Crear `entities/producto/` con types y API client (endpoints públicos del backend)
- Crear página de catálogo `/productos` con grid de productos y botón "Agregar al carrito"
- Crear `CartDrawer` (panel lateral) con `CartSummary` mostrando items, cantidades, subtotales y total
- Integrar badge con contador de items en la navegación (`Navigation.tsx`)
- Implementar exclusión de ingredientes por producto (US-030)
- Agregar ruta `/carrito` como página dedicada del carrito
- Agregar ruta `/productos` al router

## Capabilities

### New Capabilities
- `cart-ui`: Componentes de presentación del carrito (CartDrawer, CartSummary, cart badge) y página de catálogo de productos con integración al cartStore

### Modified Capabilities
<!-- None — no existing specs change behavior -->

## Impact

- **Frontend**: 4-5 archivos nuevos en `features/cart/`, 3 archivos en `entities/producto/`, 1-2 archivos modificados (Navigation, RouterProvider)
- **Backend**: Sin cambios — consume endpoints existentes de `productos/`
- **Stores**: Sin cambios — `cartStore` y `uiStore` ya tienen toda la lógica necesaria
