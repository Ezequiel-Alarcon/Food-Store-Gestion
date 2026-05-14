## Why

El dashboard administrativo de métricas necesita visualización para los 4 endpoints implementados en `admin-metrics` (backend). Sin frontend, los datos JSON de ventas, pedidos por estado, revenue y top productos no son accionables para ADMIN/GESTOR.

## What Changes

- **Nuevo:** Panel de dashboard KPIs para administración
- **Nuevo:** Tarjetas de métricas principales con valores en tiempo real
- **Nuevo:** Gráfico de ventas últimos 30 días (línea)
- **Nuevo:** Gráfico de pedidos por estado (barras)
- **Nuevo:** Lista de top 10 productos más vendidos
- **Nuevo:** Selector de rango temporal (7d, 30d, 90d) para ventas
- **Nuevo:** Indicadores de loading skeletons durante carga de datos

## Capabilities

### New Capabilities

- `admin-dashboard`: Dashboard KPIs administrativo con gráficos recharts, tarjetas de métricas y filtros temporales. Accesible solo para roles ADMIN y GESTOR.

## Impact

- **Agregados:**
  - `frontend/src/features/admin/dashboard/` — componentes dashboard
  - `frontend/src/features/admin/dashboard/components/` — MetricCard, SalesChart, OrdersByStatusChart, TopProductsTable, DateRangeSelector
  - `frontend/src/features/admin/dashboard/api/` — queries TanStack Query para métricas
  - `frontend/src/features/admin/dashboard/hooks/` — useMetrics, useSalesChart, useTopProducts
  - `frontend/src/pages/admin/DashboardPage.tsx` — página principal
  - `frontend/src/app/router.tsx` — ruta `/admin/dashboard`

- **Dependencias:**
  - Backend: endpoints de `admin-metrics` (ya archivados)
  - Frontend: `recharts` (para gráficos), `auth-frontend` (guards por rol)

- **Dependencias de ruta crítica:**
  - `admin-metrics` (backend) — ✅ archivado 2026-05-13
  - `auth-frontend` (protección de rutas) — ✅ archivado