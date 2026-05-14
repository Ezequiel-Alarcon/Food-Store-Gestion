## Context

El backend de métricas administrativas (`admin-metrics`) está implementado con 4 endpoints REST que retornan JSON con KPIs. El frontend actual no tiene ningún dashboard administrativo — la Fase 3 construye esto por primera vez.

El proyecto usa:
- **Recharts** para gráficos (ya instalado según la spec)
- **TanStack Query 5** para consumo de APIs (ya configurado en `frontend-config`)
- **Zustand stores** para estado local
- **Tailwind inline** para estilos (convención del proyecto)
- **FSD** (Feature-Sliced Design) para estructura

## Goals / Non-Goals

**Goals:**
- Dashboard KPIs en `/admin/dashboard` accesible para ADMIN y GESTOR
- 4 tarjetas de métricas: Total Pedidos, Revenue, Ticket Promedio, Clientes
- Gráfico de línea: ventas últimos 30 días
- Gráfico de barras: pedidos por estado
- Tabla: top 10 productos más vendidos
- Selector de rango temporal (7d, 30d, 90d) para el gráfico de ventas
- Loading skeletons mientras cargan los datos
- Proteger ruta con `ProtectedRoute` (solo ADMIN/GESTOR)

**Non-Goals:**
- No se modifica el backend
- No se crea página de pedidos admin (change 20 `orders-list-gestor-frontend`)
- No se crea página de usuarios admin (change 21 `users-admin-frontend`)
- No se implementa exportación de datos (PDF/CSV) — fuera de scope
- No se implementa refresh automático de métricas — polling manual con botón

## Decisions

### 1. Componentes vs inline Tailwind

**Decision:** Usar componentes separados para cada elemento del dashboard.

**Rationale:** El dashboard es más complejo que auth (gráficos, tablas, cards). Separar componentes facilita mantenimiento y testing. Las props fluyen top-down: `DashboardPage` → `MetricCard` + `SalesChart` + `OrdersByStatusChart` + `TopProductsTable`.

**Alternatives:** Inline en la página → descartado porque el componente sería >300 líneas.

### 2. Selector de rango temporal: estado local vs URL param

**Decision:** Estado local con `useState` (7d default).

**Rationale:** Simplicidad. El usuario hace click en un botón y el gráfico se actualiza. No necesitamos persistir el filtro en la URL para esta versión.

**Alternatives:** URL params (`?range=30d`) → overkill para v1, se puede agregar en future iterations.

### 3. Datos del gráfico de ventas: hardcoded 30 días vs parámetro

**Decision:** El endpoint `/admin/metrics/sales-chart/` hardcodea 30 días en backend. El frontend recibe esos datos y filtra localmente según el selector.

**Rationale:** El backend ya está implementado así. Filtrar en frontend es más rápido que modificar el backend para pasar un parámetro. Trade-off: se descargan 30 días siempre aunque el usuario seleccione 7d.

**Alternatives:** Modificar backend para aceptar `?days=` → requiere cambiar Change 17 (backend), no vale la pena para este scope.

### 4. Estructura de archivos

**Decision:** Crear `features/admin/dashboard/` con subcarpetas `components/`, `api/`, `hooks/`.

```
frontend/src/features/admin/dashboard/
├── index.ts                    # barrel export
├── DashboardPage.tsx           # página principal
├── components/
│   ├── MetricCard.tsx           # tarjeta KPI individual
│   ├── SalesChart.tsx           # gráfico de línea (recharts)
│   ├── OrdersByStatusChart.tsx # gráfico de barras (recharts)
│   ├── TopProductsTable.tsx    # tabla ranking productos
│   ├── DateRangeSelector.tsx   # selector 7d/30d/90d
│   └── DashboardSkeleton.tsx   # loading skeleton
├── api/
│   └── metricsApi.ts           # queries TanStack Query
└── hooks/
    └── useMetrics.ts           # hook compuesto (datos + estado)
```

**Rationale:** Separa concerns: API layer (queries), hook (lógica de estado), componentes (UI). Consistente con FSD y con cambios anteriores como `cart-frontend`.

### 5. Tipos TypeScript

**Decision:** Crear types locales (`MetricsTypes.ts`) que mapean los schemas del backend.

```typescript
interface GeneralMetrics {
  total_pedidos: number;
  total_revenue: number;
  ticket_promedio: number;
  total_clientes: number;
}

interface SalesChartEntry {
  fecha: string;  // ISO date string
  total_pedidos: number;
  revenue: number;
}

interface TopProductEntry {
  producto_id: number;
  nombre: string;
  cantidad_vendida: number;
}

interface OrdersByStatusEntry {
  estado_codigo: string;
  cantidad: number;
}
```

**Rationale:** Tipos explícitos > inferencia automática. Facilita debug y autocompletado.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Gráfico vacío si no hay pedidos | Mostrar mensaje "Sin datos aún" con placeholder de recharts |
| Error de red en métricas | Try/catch en queries + mensaje de error en UI |
| Datos negativos o NaN | Backend debería asegurar valores válidos, pero frontend también valida antes de renderizar |
| Performance con muchos datos | Recharts maneja datasets grandes bien; si hay problema, implementar virtualización |

## API Endpoints Consumidos

| Endpoint | Method | Query Params | Response |
|----------|--------|--------------|----------|
| `/api/v1/admin/metrics/` | GET | — | `GeneralMetricsResponse` |
| `/api/v1/admin/metrics/sales-chart/` | GET | — | `SalesChartResponse` |
| `/api/v1/admin/metrics/top-products/` | GET | — | `TopProductEntry[]` |
| `/api/v1/admin/metrics/orders-by-status/` | GET | — | `OrdersByStatusEntry[]` |

**Auth:** Bearer token JWT (ADMIN o GESTOR role).

## Dependencias

- `recharts` — gráficos (verificar en `package.json`)
- `@tanstack/react-query` — data fetching (ya en proyecto)
- `frontend/src/features/auth/` — ProtectedRoute (ya existe)
- Backend: Change 17 `admin-metrics` archivado ✅