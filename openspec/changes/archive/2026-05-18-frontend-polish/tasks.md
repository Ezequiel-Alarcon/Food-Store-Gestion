# Tasks: frontend-polish

> **Objetivo:** Pulir UX para la demo: TanStack Query en OrdersPage, búsqueda server-side, estados de pago claros.

## 1. OrdersPage — TanStack Query + polling

- [x] 1.1 OrdersPage → `useQuery` con `queryKey: ['mis-pedidos', page, estado]`
- [x] 1.2 `refetchInterval: 30000` polling automático
- [x] 1.3 `isLoading` → skeleton, `isError` → mensaje de error
- [x] 1.4 Filtro por estado y paginación mantenidos
- [x] 2.1 Debounced search (300ms) en CatalogPage
- [x] 2.2 `search` como query param al backend
- [x] 2.3 `filter()` local eliminado
- [x] 2.4 "Buscando..." mientras debounce activo
- [x] 3.1 UI `pending`: ⏳ fondo amarillo
- [x] 3.2 UI `in_process`: 🔄 fondo azul
- [x] 3.3 UI `cancelled`: ⊘ fondo gris, botón reintentar
- [x] 3.4 `approved` ✅ verde y `rejected` ❌ rojo mantenidos
- [x] 4.1-4.4 Verificación + archive + engram sync + rama + commit + push
