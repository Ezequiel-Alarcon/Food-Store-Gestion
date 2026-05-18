# Design: frontend-orders-feature

## Approach

Movida directa sin refactor de lógica. El archivo se traslada tal cual está.

```
Antes:
  pages/OrdersPage.tsx          ← lógica + UI del feature "Mis Pedidos"
  features/orders/.gitkeep      ← vacío

Después:
  features/orders/OrdersPage.tsx ← lógica + UI del feature "Mis Pedidos"  
  features/orders/index.ts       ← barrel export
```

## Files affected

| Acción | Archivo |
|--------|---------|
| MOVER | `pages/OrdersPage.tsx` → `features/orders/OrdersPage.tsx` |
| CREAR | `features/orders/index.ts` (barrel export) |
| ELIMINAR | `features/orders/.gitkeep` |
| EDITAR | `providers/RouterProvider.tsx` (línea 14 — actualizar import path) |

## Imports

El archivo movido importa de `../entities/pedido`. Al moverse de `pages/` a `features/orders/`, la ruta relativa cambia:

- `../entities/pedido` → `../../entities/pedido`

El RouterProvider import cambia:

- `'../pages/OrdersPage'` → `'../features/orders'` (usa el barrel index)
