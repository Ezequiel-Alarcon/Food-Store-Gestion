## Context

El backend del change 15 (`orders-list-gestor`) ya expone los endpoints:
- `GET /api/v1/admin/pedidos` — lista todos los pedidos con filtros
- `GET /api/v1/admin/pedidos/{id}` — detalle de un pedido específico

Los roles autorizados son ADMIN y GESTOR_PEDIDOS. El frontend actual no tiene ninguna interfaz para que estos roles gestionen pedidos.

## Goals / Non-Goals

**Goals:**
- Crear página `/admin/pedidos` con tabla de pedidos
- Permitir filtrar por estado de pedido (PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO)
- Permitir buscar por nombre del cliente
- Crear página de detalle `/admin/pedidos/:id` con toda la info del pedido
- Mostrar timeline de transiciones de estado

**Non-Goals:**
- Modificar estados de pedido desde frontend (eso sería change futuro)
- Crear dashboard con gráficos (eso es change 22 `admin-metrics-frontend`)
- Exportar a PDF/Excel

## Decisions

1. **Tabla con TanStack Table**: Usar TanStack Table para la lista — ya está instalado en el proyecto y permite sorting, pagination, filtering robusto.

2. **Filtros en URL**: Los filtros se persistirán en la URL (query params) para permitir compartir enlaces filtrados.

3. **Estados como badges**: Cada estado tendrá un badge con color según el tipo:
   - PENDIENTE: yellow
   - CONFIRMADO: blue
   - EN_PREP: purple
   - EN_CAMINO: indigo
   - ENTREGADO: green
   - CANCELADO: red

4. **Skeleton loading**: Mientras cargan los datos, mostrar skeletons para mejor UX.

## Risks / Trade-offs

- **[Riesgo] Backend no responde**: Mostrar mensaje de error claro con botón de reintento.
- **[Riesgo] Lista muy grande**: Pagination en backend con 20 items por página.
- **[Trade-off]阅**: Decodificar timestamps a formato local argentino (DD/MM/YYYY HH:mm).