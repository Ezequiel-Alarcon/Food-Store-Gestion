/**
 * Gráfico de línea para ventas diarias usando Recharts.
 * Muestra revenue y cantidad de pedidos por día.
 */
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import type { SalesChartEntry } from '../types'

interface SalesChartProps {
  data: SalesChartEntry[]
  dateRange: 7 | 30 | 90
  isLoading?: boolean
}

/**
 * Formatea la fecha para el eje X.
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
  })
}

/**
 * Formatea el valor monetario para el Tooltip.
 */
function formatCurrency(value: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

interface CustomTooltipProps {
  active?: boolean
  payload?: Array<{ name: string; value: number; color: string }>
  label?: string
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload?.length) return null

  return (
    <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
      <p className="font-medium text-gray-700 mb-1">{formatDate(label || '')}</p>
      {payload.map((entry, index) => (
        <p key={index} className="text-sm" style={{ color: entry.color }}>
          {entry.name}: {entry.name === 'Revenue' ? formatCurrency(entry.value) : entry.value}
        </p>
      ))}
    </div>
  )
}

/**
 * Gráfico de ventas que muestra revenue y pedidos por día.
 * Filtra los datos según el rango de fechas seleccionado.
 */
export function SalesChart({ data, dateRange, isLoading }: SalesChartProps) {
  // Filtrar datos según el rango de fechas
  // El backend retorna 30 días, filtramos en frontend
  const filteredData = (() => {
    if (!data || data.length === 0) return []
    const daysToShow = dateRange
    return data.slice(-daysToShow)
  })()

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-48 mb-4" />
        <div className="h-64 bg-gray-100 rounded" />
      </div>
    )
  }

  if (!data || filteredData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Ventas por Día</h3>
        <div className="h-64 flex items-center justify-center text-gray-500">
          <p>No hay datos de ventas disponibles</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Ventas por Día</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={filteredData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="fecha"
              tickFormatter={formatDate}
              stroke="#6b7280"
              fontSize={12}
              tickMargin={8}
            />
            <YAxis
              yAxisId="left"
              stroke="#6b7280"
              fontSize={12}
              tickFormatter={(value) => `$${value.toLocaleString()}`}
              tickMargin={8}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#6b7280"
              fontSize={12}
              tickMargin={8}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="revenue"
              name="Revenue"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#6366f1' }}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="total_pedidos"
              name="Pedidos"
              stroke="#10b981"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#10b981' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}