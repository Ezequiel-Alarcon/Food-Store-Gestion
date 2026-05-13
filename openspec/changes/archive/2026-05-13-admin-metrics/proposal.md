## Why

El panel de administración necesita métricas KPIs para que ADMIN y GESTOR puedan tomar decisiones basadas en datos: ventas, productos más vendidos, estado de pedidos. El módulo `admin/` existe con archivos vacíos (`schemas.py`, `router.py`) — este change lo completa con endpoints de métricas.

## What Changes

1. **Endpoints de métricas** en `admin/router.py`:
   - `GET /api/v1/admin/metrics/` — métricas generales (total pedidos, revenue, usuarios activos)
   - `GET /api/v1/admin/metrics/sales-chart/` — datos para gráfico de ventas (últimos 30 días)
   - `GET /api/v1/admin/metrics/top-products/` — top 10 productos más vendidos
   - `GET /api/v1/admin/metrics/orders-by-status/` — conteo de pedidos por estado

2. **Schemas de respuesta** en `admin/schemas.py` — Pydantic v2 response models para cada endpoint

3. **Lógica de negocio** en `admin/service.py` — queries agregadas a la BD

4. **Tests de integración** cubriendo los 4 endpoints con auth de ADMIN/GESTOR

## Capabilities

### New Capabilities
- `admin-metrics`: Endpoints REST para dashboard KPIs — métricas generales, gráfico de ventas, top productos, pedidos por estado. Acceso: ADMIN, GESTOR.

### Modified Capabilities
- (ninguno)

## Impact

- **Code:** `backend/app/modules/admin/{schemas.py, router.py, service.py, repository.py}` (completar implementación)
- **Tests:** `backend/tests/modules/admin/` (nuevo directorio)
- **Dependencies:** Depende de `orders-fsm` (change 13, ✅ archivado) y `users-admin` (change 16, ✅ archivado) — modelos Pedido y Usuario disponibles