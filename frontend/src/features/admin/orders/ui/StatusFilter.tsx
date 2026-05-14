import { ESTADOS, ESTADO_LABELS } from './constants'

interface StatusFilterProps {
  value: string
  onChange: (value: string) => void
}

export function StatusFilter({ value, onChange }: StatusFilterProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
    >
      <option value="">Todos los estados</option>
      {ESTADOS.map((estado) => (
        <option key={estado} value={estado}>
          {ESTADO_LABELS[estado]}
        </option>
      ))}
    </select>
  )
}