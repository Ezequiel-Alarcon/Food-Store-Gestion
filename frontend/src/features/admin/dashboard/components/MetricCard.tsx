import type { ReactNode } from 'react'

interface MetricCardProps {
  title: string
  value: string | number
  icon: ReactNode
  description?: string
  isLoading?: boolean
}

/**
 * Tarjeta KPI individual para el dashboard de métricas.
 * Muestra un título, valor destacado, icono y descripción opcional.
 */
export function MetricCard({ title, value, icon, description, isLoading }: MetricCardProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="flex items-center justify-between mb-4">
          <div className="h-4 bg-gray-200 rounded w-24" />
          <div className="h-8 w-8 bg-gray-200 rounded" />
        </div>
        <div className="h-8 bg-gray-200 rounded w-32 mb-2" />
        {description && <div className="h-3 bg-gray-100 rounded w-40" />}
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</h3>
        <div className="text-gray-400">{icon}</div>
      </div>
      <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
      {description && <p className="text-sm text-gray-500">{description}</p>}
    </div>
  )
}