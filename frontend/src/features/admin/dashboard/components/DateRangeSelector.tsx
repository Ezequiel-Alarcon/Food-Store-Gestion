/**
 * Selector de rango temporal para filtrar el gráfico de ventas.
 */
import type { DateRange } from '../types'

interface DateRangeSelectorProps {
  value: DateRange
  onChange: (range: DateRange) => void
}

const RANGES: { value: DateRange; label: string }[] = [
  { value: 7, label: '7 días' },
  { value: 30, label: '30 días' },
  { value: 90, label: '90 días' },
]

/**
 * Botones para seleccionar el rango de fechas a mostrar en el gráfico de ventas.
 * Solo afecta al SalesChart, no a las métricas generales.
 */
export function DateRangeSelector({ value, onChange }: DateRangeSelectorProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-500 mr-2">Rango:</span>
      {RANGES.map((range) => (
        <button
          key={range.value}
          onClick={() => onChange(range.value)}
          className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
            value === range.value
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          {range.label}
        </button>
      ))}
    </div>
  )
}