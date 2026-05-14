/**
 * Página principal del dashboard de métricas administrativas.
 * Muestra KPIs, gráficos y rankings para ADMIN y GESTOR.
 */
import { ProtectedRoute } from '../../auth/ProtectedRoute'
import { useMetrics } from './hooks/useMetrics'
import { MetricCard } from './components/MetricCard'
import { SalesChart } from './components/SalesChart'
import { OrdersByStatusChart } from './components/OrdersByStatusChart'
import { TopProductsTable } from './components/TopProductsTable'
import { DateRangeSelector } from './components/DateRangeSelector'
import { DashboardSkeleton } from './components/DashboardSkeleton'

// Iconos SVG inline para las métricas
const ShoppingBagIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
  </svg>
)

const CurrencyIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
)

const TicketIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
  </svg>
)

const UsersIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
)

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

function formatNumber(num: number): string {
  return num.toLocaleString('es-AR')
}

function DashboardContent() {
  const {
    metrics,
    salesChart,
    topProducts,
    ordersByStatus,
    isLoading,
    isError,
    error,
    refetch,
    dateRange,
    setDateRange,
  } = useMetrics()

  if (isLoading) {
    return <DashboardSkeleton />
  }

  if (isError) {
    return (
      <div className="p-8 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h2 className="text-lg font-semibold text-red-800 mb-2">Error al cargar métricas</h2>
          <p className="text-red-600 mb-4">
            {error?.message || 'No se pudieron cargar los datos del dashboard'}
          </p>
          <button
            onClick={refetch}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Reintentar
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard de Métricas</h1>
          <p className="text-gray-600 mt-1">Resumen del rendimiento del negocio</p>
        </div>
        <div className="flex items-center gap-4">
          <DateRangeSelector value={dateRange} onChange={setDateRange} />
          <button
            onClick={refetch}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refrescar
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="Total Pedidos"
          value={metrics ? formatNumber(metrics.total_pedidos) : '-'}
          icon={<ShoppingBagIcon />}
          description="Pedidos completados"
        />
        <MetricCard
          title="Revenue Total"
          value={metrics ? formatCurrency(metrics.total_revenue) : '-'}
          icon={<CurrencyIcon />}
          description="Ingresos acumulados"
        />
        <MetricCard
          title="Ticket Promedio"
          value={metrics ? formatCurrency(metrics.ticket_promedio) : '-'}
          icon={<TicketIcon />}
          description="Promedio por pedido"
        />
        <MetricCard
          title="Clientes Activos"
          value={metrics ? formatNumber(metrics.total_clientes) : '-'}
          icon={<UsersIcon />}
          description="Con pedidos realizados"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <SalesChart
          data={salesChart?.datos || []}
          dateRange={dateRange}
        />
        <OrdersByStatusChart data={ordersByStatus || []} />
      </div>

      {/* Top Products */}
      <TopProductsTable data={topProducts || []} />
    </div>
  )
}

export function DashboardPage() {
  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'GESTOR']}>
      <DashboardContent />
    </ProtectedRoute>
  )
}