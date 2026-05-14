## Context

El backend expone `GET /api/v1/pedidos/` (listado paginado con filtros) y `GET /api/v1/pedidos/{id}` (detalle). Para CLIENT, el listado solo devuelve sus propios pedidos. El detalle incluye items, dirección de entrega, estado, total e historial.

## Goals / Non-Goals

**Goals:**
- Mostrar lista de pedidos del cliente con paginación y filtro por estado
- Ver detalle de un pedido (items, cantidades, dirección, total, estado)
- Diseño responsive y consistente con el resto de la app

**Non-Goals:**
- No se modifica backend
- No se implementa cancelación de pedidos (ya existe el endpoint pero no el UI)
- No se toca el panel admin de pedidos

## Decisions

### D1: Lista de pedidos como tabla/cards responsive

En mobile se muestran como cards apiladas, en desktop como tabla. Cada fila muestra: ID, fecha, estado (con badge de color), total, items count.

### D2: Detalle de pedido como sección expandible o página dedicada

Se usa una página dedicada `/pedidos/:id` o un drawer/modal. Drawer es mejor UX para no perder el contexto de la lista.

### D3: Estados con badges de colores

PENDIENTE → amarillo, CONFIRMADO → verde, EN_PREPARACION → azul, EN_CAMINO → naranja, ENTREGADO → verde oscuro, CANCELADO → rojo.
