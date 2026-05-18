# Design: frontend-polish

## Context

Tres componentes frontend necesitan pulido para la demo: OrdersPage (sin TanStack Query, sin polling), CatalogPage (búsqueda solo local), PaymentResult (estados confusos).

## Goals / Non-Goals

**Goals:**
- OrdersPage con `useQuery` + `refetchInterval: 30000`
- CatalogPage con búsqueda server-side (debounced, 300ms)
- PaymentResult con UI diferenciada por estado de pago

**Non-Goals:**
- NO modificar backend
- NO cambiar APIs

## Decisions

### OrdersPage — useQuery + polling
Reemplazar `useState`/`useEffect`/`fetchOrders` por `useQuery` con `queryKey: ['mis-pedidos', page, estado]` y `refetchInterval: 30000`. Esto da caché automático, estados de carga/error, y polling cada 30s para ver cambios de estado en tiempo real.

### CatalogPage — search server-side
Agregar debounced search (300ms) que envía `?search=term` al backend `GET /api/v1/productos/catalogo`. Eliminar el `filter()` local. El backend ya soporta el parámetro `search`.

### PaymentResult — estados claros
Mapear cada estado MP a UI específica:
- `approved` → ✅ verde, "Pago aprobado"
- `pending` → ⏳ amarillo, "Pago pendiente de acreditación"
- `in_process` → 🔄 azul, "Pago en revisión por MercadoPago"
- `rejected` → ❌ rojo, con mensaje específico del `status_detail`
- `cancelled` → ⊘ gris, "Pago cancelado"

## Risks
- Polling 30s puede generar tráfico innecesario si hay muchos usuarios → Aceptable para MVP
- Debounced search agrega 300ms de latencia → Mejor UX que búsqueda incompleta
