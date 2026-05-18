# Spec: ux-polish

> **Tipo:** Mejora de UX (sin cambios de API)  
> **Cambio padre:** `frontend-polish`

## Requisitos

### RQ-UX01 — OrdersPage con TanStack Query
- `useQuery` con `queryKey: ['mis-pedidos', page, estado]`
- `refetchInterval: 30000` para polling de estados
- Skeleton loader mientras carga
- Mensaje de error si falla

### RQ-UX02 — Búsqueda server-side en catálogo
- Debounced search (300ms) → query param `?search=term`
- Eliminar filtro local
- Indicador "Buscando..." durante debounce

### RQ-UX03 — Estados de pago diferenciados
- `approved` → verde ✅
- `pending` → amarillo ⏳
- `in_process` → azul 🔄
- `rejected` → rojo ❌
- `cancelled` → gris ⊘
