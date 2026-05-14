/**
 * Gráfico de barras para pedidos por estado usando Recharts.
 */
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import type { OrdersByStatusEntry } from '../types'

interface OrdersByStatusChartProps {
  data: OrdersByStatusEntry[]
  isLoading?: boolean
}

// Colores por estado
const STATUS_COLORS: Record<string, string> = {
  PENDIENTE: '#f59e0b', // amber
  CONFIRMADO: '#3b82f6', // blue
  EN_PREP: '#8b5cf6', // violet
  EN_CAMINO: '#6366f1', // indigo
  ENTREGADO: '#10b981', // green
  CANCELADO: '#ef4444', // red
}

// Labels descriptivos para estados
const STATUS_LABELS: Record<string, string> = {
  PENDIENTE: 'Pendiente',
  CONFIRMADO: 'Confirmado',
  EN_PREP: 'En Preparación',
  EN_CAMINO: 'En Camino',
  ENTREGADO: 'Entregado',
  CANCELADO: 'Cancelado',
}

interface CustomTooltipProps {
  active?: boolean
  payload?: Array<{ value: number; payload: OrdersByStatusEntry }>
}

function CustomTooltip({ active, payload }: CustomTooltipProps) {
  if (!active || !payload?.length) return null

  const entry = payload[0].payload
  const label = STATUS_LABELS[entry.estado_codigo] || entry.estado_codigo

  return (
    <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
      <p className="font-medium text-gray-700">{label}</p>
      <p className="text-sm text-gray-500">{payload[0].value} pedidos</p>
    </div>
  )
}

/**
 * Gráfico de barras que muestra la distribución de pedidos por estado.
 */
export function OrdersByStatusChart({ data, isLoading }: OrdersByStatusChartProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-40 mb-4" />
        <div className="h-64 bg-gray-100 rounded" />
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Pedidos por Estado</h3>
        <div className="h-64 flex items-center justify-center text-gray-500">
          <p>No hay datos de pedidos por estado</p>
        </div>
      </div>
    )
  }

  // Mapear datos para el chart con labels descriptivos
  const chartData = data.map((entry) => ({
    ...entry,
    label: STATUS_LABELS[entry.estado_codigo] || entry.estado_codigo,
    color: STATUS_COLORS[entry.estado_codigo] || '#6b7280',
  }))

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Pedidos por Estado</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="label" stroke="#6b7280" fontSize={12} tickMargin={8} />
            <YAxis stroke="#6b7280" fontSize={12} tickMargin={8} allowDecimals={false} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="cantidad" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      {/* Leyenda */}
      <div className="mt-4 flex flex-wrap gap-2">
        {chartData.map((entry) => (
          <div key={entry.estado_codigo} className="flex items-center gap-1 text-xs">
            <span
              className="w-3 h-3 rounded"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-gray-600">
              {entry.label}: {entry.cantidad}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}