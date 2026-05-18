# Proposal: frontend-orders-feature

## What
Mover `OrdersPage.tsx` de `pages/` a `features/orders/` para cumplir con la arquitectura FSD (Feature-Sliced Design).

## Why
El proyecto sigue FSD estricto: las páginas deben delegar en features, no contener lógica de negocio directamente. `OrdersPage` vive en `pages/` y contiene lógica de UI, filtrado, y detalle que pertenece al feature `orders`. El directorio `features/orders/` ya existe (vacío, solo `.gitkeep`) y es el lugar correcto.

## Scope
- **Archivos:** ~3 modificados
- **Riesgo:** Bajo — solo se mueve el archivo y se actualiza 1 import

## Dependencies
- Ninguna (change independiente de Fase 4)
