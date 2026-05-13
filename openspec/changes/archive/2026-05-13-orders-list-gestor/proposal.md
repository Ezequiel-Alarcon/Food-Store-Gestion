## Why

El rol **Gestor de Pedidos (PEDIDOS)** necesita un listado operativo de pedidos para poder priorizar, avanzar estados y detectar bloqueos (pagos pendientes, demoras, cancelaciones). Hoy la especificacion cubre pedidos en general, pero no define de forma precisa el **listado para PEDIDOS** con filtros, paginacion, RBAC y modelos de respuesta orientados a operacion.

## What Changes

- Se especifica un endpoint de **listado de pedidos para rol PEDIDOS** (backend) con:
- Paginacion estandar del sistema.
- Filtros operativos (por estado, rango de fechas, busqueda por identificador / cliente, etc.).
- Ordenamiento por fecha y/o prioridad operativa.
- Modelos de respuesta (lista y item resumido) y errores RFC 7807.
- Reglas RBAC: acceso a todos los pedidos para PEDIDOS (y ADMIN) sin exponer acciones o datos fuera de alcance.

## Capabilities

### New Capabilities
- `orders-list-gestor`: Listado backend de pedidos para rol PEDIDOS con filtros, paginacion, ordenamiento, RBAC y response models.

### Modified Capabilities

<!-- None -->

## Impact

- Backend: modulo `pedidos` (router/service/repository/schemas) para exponer un listado enriquecido para operacion.
- Seguridad: uso de `require_role([ADMIN, PEDIDOS])` y reglas de visibilidad (PEDIDOS/ADMIN ven todos; CLIENT solo propios queda fuera de este change).
- API: documentacion OpenAPI para `GET /api/v1/pedidos` (o ruta equivalente) con query params nuevos.
- Contratos: consistencia con paginacion global y errores RFC 7807.
