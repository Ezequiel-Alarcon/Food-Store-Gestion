import { useState, useEffect } from 'react'

interface Categoria {
  id: number
  nombre: string
  categoria_padre_id: number | null
  nivel?: number
  activa: boolean
}

interface CategoriesModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: { nombre: string; categoria_padre_id: number | null }) => void
  categorias: Categoria[]
  initialData?: { nombre: string; categoria_padre_id: number | null }
  editingId?: number | null
  isPending?: boolean
}

export function CategoriesModal({
  isOpen,
  onClose,
  onSave,
  categorias,
  initialData,
  editingId,
  isPending = false,
}: CategoriesModalProps) {
  const [nombre, setNombre] = useState('')
  const [parentId, setParentId] = useState<number | null>(null)

  useEffect(() => {
    if (initialData) {
      setNombre(initialData.nombre)
      setParentId(initialData.categoria_padre_id)
    } else {
      setNombre('')
      setParentId(null)
    }
  }, [initialData, isOpen])

  if (!isOpen) return null

  const isEdit = !!initialData

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nombre.trim()) return
    // Si es edición y se selecciona "Ninguna (raíz)", enviar 0 para que el backend lo interprete como "set to root"
    const parentValue = isEdit && parentId === null ? 0 : parentId
    onSave({ nombre: nombre.trim(), categoria_padre_id: parentValue })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            {isEdit ? 'Editar categoría' : 'Nueva categoría'}
          </h3>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="px-6 py-4 space-y-4">
            <div>
              <label htmlFor="cat-nombre" className="block text-sm font-medium text-gray-700 mb-1">
                Nombre
              </label>
              <input
                id="cat-nombre"
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Ej: Bebidas"
              />
            </div>

            <div>
              <label htmlFor="cat-parent" className="block text-sm font-medium text-gray-700 mb-1">
                Categoría padre
              </label>
              <select
                id="cat-parent"
                value={parentId ?? ''}
                onChange={(e) => {
                  const val = e.target.value
                  const newId = val ? Number(val) : null
                  if (newId === editingId) {
                    // No permitir seleccionarse a sí misma
                    return
                  }
                  setParentId(newId)
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="">Ninguna (raíz)</option>
                {categorias
                  .filter((c) => editingId == null || c.id !== editingId)
                  .map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {'\u00A0'.repeat((cat.nivel ?? 0) * 2)}{cat.nombre}
                    </option>
                  ))}
              </select>
              {editingId != null && parentId === editingId ? (
                <p className="text-red-500 text-xs mt-1">Una categoría no puede ser padre de sí misma</p>
              ) : (
                <p className="text-gray-400 text-xs mt-1">
                  {editingId != null ? 'No puede seleccionar la misma categoría como padre' : ''}
                </p>
              )}
            </div>
          </div>

          <div className="px-6 py-4 bg-gray-50 flex justify-end gap-3 rounded-b-lg">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={!nombre.trim() || isPending}
              className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700 disabled:opacity-50"
            >
              {isPending ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
