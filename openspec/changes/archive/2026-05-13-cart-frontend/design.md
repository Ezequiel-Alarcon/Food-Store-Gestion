## Context

El frontend de Food Store está en sus etapas iniciales. La Fase 0-1 completó auth (login/register) y la Fase 2 completó todo el backend. Ahora en Fase 3 se construye la experiencia del cliente.

El `cartStore.ts` ya está implementado con Zustand + persistencia localStorage. Contiene:
- `items: CartItem[]` con producto, cantidad y personalización
- Acciones: `addItem`, `removeItem`, `updateQuantity`, `clearCart`
- Selectores: `selectItems`, `totalItems()`, `totalPrice()`, `getItem(id)`

El `uiStore.ts` ya tiene `cartOpen` y `openCart/closeCart/toggleCart` esperando ser usados por un CartDrawer.

El backend expone endpoints públicos de productos (`GET /api/v1/productos`, `GET /api/v1/productos/{id}`) que necesitan su contraparte frontend.

## Goals / Non-Goals

**Goals:**
- Crear `entities/producto/` (types + API client) para consumir el backend de productos
- Construir página de catálogo accesible en `/productos` con grid responsive
- Implementar `CartDrawer` como panel lateral con `CartSummary`
- Integrar badge de items en la navegación
- Soportar exclusión de ingredientes al agregar productos (US-030)

**Non-Goals:**
- No se modifica el `cartStore` (ya está completo)
- No se toca el backend
- No se implementa checkout (es el change `payments-integration` frontend, fuera de scope)
- No se crean componentes shared UI genéricos (se usa Tailwind inline como en auth)

## Decisions

### D1: CartDrawer como panel lateral (no modal ni página)

El `uiStore` ya modela `cartOpen` como booleano, lo que sugiere un drawer/panel lateral. Un drawer es mejor UX para e-commerce: permite seguir viendo el catálogo mientras se revisa el carrito. Se usa un panel con `fixed right-0` + overlay con backdrop.

**Alternativa considerada:** Modal centrado → descartado porque bloquea la vista del catálogo.

### D2: Entidad Producto mínima (solo endpoints públicos)

El backend tiene endpoints completos de productos (CRUD admin + catálogo público). Para el carrito solo necesitamos los endpoints públicos: listar y detalle. Los tipos se limitan a `ProductoCatalogo` (nombre, precio, imagen, stock, categorías, ingredientes).

### D3: Catálogo de productos como página independiente

La ruta `/productos` muestra el catálogo completo con filtros y grid. Cada producto tiene un botón "Agregar" que llama a `cartStore.addItem()`. El diseño sigue el patrón de grid de Tailwind responsive (1 col mobile, 2 tablet, 3 desktop).

### D4: Exclusión de ingredientes con checkboxes en modal

Cuando el producto tiene ingredientes, se muestra un modal con checkboxes antes de agregar al carrito. Los IDs de ingredientes excluidos se pasan como `personalizacion` al `cartStore.addItem()`.

### D5: Sin componentes shared UI

Los forms de auth usan Tailwind inline. Seguimos el mismo patrón para mantener consistencia y evitar el overhead de crear un design system ahora. Los componentes del carrito usan clases Tailwind directamente.

## Risks / Trade-offs

- **[Riesgo] La página de catálogo sin paginación puede ser lenta con muchos productos** → Mitigación: El backend ya soporta `?page=&size=`, se implementa paginación básica desde el inicio.
- **[Riesgo] Sin componentes shared, hay duplicación de estilos** → Mitigación: Es aceptable en esta etapa. Se refactoriza cuando se cree el design system (fuera de scope).
