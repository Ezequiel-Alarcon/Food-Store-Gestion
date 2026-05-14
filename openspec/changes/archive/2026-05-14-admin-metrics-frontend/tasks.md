## 1. Estructura y Tipos

- [x] 1.1 Crear directorio `frontend/src/features/admin/dashboard/components/`
- [x] 1.2 Crear directorio `frontend/src/features/admin/dashboard/api/`
- [x] 1.3 Crear directorio `frontend/src/features/admin/dashboard/hooks/`
- [x] 1.4 Crear `frontend/src/features/admin/dashboard/types.ts` con interfaces: `GeneralMetrics`, `SalesChartEntry`, `TopProductEntry`, `OrdersByStatusEntry`

## 2. API Layer (TanStack Query)

- [x] 2.1 Crear `api/metricsApi.ts` con queries:
  - `useGeneralMetrics()` → GET `/api/v1/admin/metrics/`
  - `useSalesChart()` → GET `/api/v1/admin/metrics/sales-chart/`
  - `useTopProducts()` → GET `/api/v1/admin/metrics/top-products/`
  - `useOrdersByStatus()` → GET `/api/v1/admin/metrics/orders-by-status/`
- [x] 2.2 Exportar todas las queries desde `api/index.ts`

## 3. Hook Compuesto

- [x] 3.1 Crear `hooks/useMetrics.ts` que combine las 4 queries y exponga:
  - `metrics` (datos generales)
  - `salesChart` (filtrado por rango)
  - `topProducts`
  - `ordersByStatus`
  - `dateRange` (estado local: 7d | 30d | 90d)
  - `setDateRange(range)` (setter)
  - `isLoading`, `error`

## 4. Componentes UI

- [x] 4.1 Crear `MetricCard.tsx` — props: `title`, `value`, `icon`, `description`
- [x] 4.2 Crear `SalesChart.tsx` — gráfico de línea con recharts (LineChart), filtrado por `dateRange`
- [x] 4.3 Crear `OrdersByStatusChart.tsx` — gráfico de barras con recharts (BarChart)
- [x] 4.4 Crear `TopProductsTable.tsx` — tabla con ranking productos más vendidos
- [x] 4.5 Crear `DateRangeSelector.tsx` — botones: 7 días, 30 días, 90 días
- [x] 4.6 Crear `DashboardSkeleton.tsx` — skeletons de carga (3 cards + 2 charts + tabla)

## 5. Página Principal

- [x] 5.1 Crear `DashboardPage.tsx` con ProtectedRoute (solo ADMIN/GESTOR)
- [x] 5.2 Implementar layout: grid 4 MetricCards → 2 charts → TopProductsTable
- [x] 5.3 Integrar `useMetrics()` hook y `DashboardSkeleton` durante loading
- [x] 5.4 Agregar botón de "Refrescar" para re-fetch manual

## 6. Routing

- [x] 6.1 Agregar ruta en `frontend/src/providers/RouterProvider.tsx`:
  - `/admin/dashboard` → `DashboardPage`
  - Proteger con `ProtectedRoute` roles ADMIN y GESTOR
- [x] 6.2 Verificar link en navegación admin (usa navegación existente)

## 7. Dependencias

- [x] 7.1 Verificar que `recharts` está en `package.json` ✅ (ya instalado)
- [x] 7.2 Instalar dependencias si se agregaron — N/A (no se agregaron)

## 8. Verificación

- [x] 8.1 Correr TypeScript: `cd frontend && npx tsc --noEmit` ✅ (sin errores en dashboard)
- [x] 8.2 Verificar build: `cd frontend && npm run build` ✅ (build exitoso)
- [x] 8.3 Probar manualmente: login como ADMIN, ir a `/admin/dashboard`, verificar gráficos y datos ✅
- [x] 8.4 Probar acceso: ADMIN tiene acceso ✅, menú de navegación arreglado para ADMIN y GESTOR ✅