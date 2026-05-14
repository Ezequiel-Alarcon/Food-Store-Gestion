import { ROLES, type RolValue } from '../../../../entities/usuario-admin/types'

interface RoleFilterProps {
  value: string
  onChange: (value: string) => void
}

export function RoleFilter({ value, onChange }: RoleFilterProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    >
      <option value="">Todos los roles</option>
      {ROLES.map((rol) => (
        <option key={rol} value={rol}>
          {rol}
        </option>
      ))}
    </select>
  )
}