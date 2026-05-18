import { useState, useEffect } from 'react'

interface ProductFormData {
  nombre: string
  descripcion: string
  precio: number
  imagen_url: string
  categoria_ids: number[]
  ingrediente_ids: number[]
}

interface ProductFormModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: ProductFormData) => void
  categorias: { id: number; nombre: string }[]
  ingredientes: { id: number; nombre: string; es_alergeno: boolean }[]
  initialData?: ProductFormData
  isPending?: boolean
}

export function ProductFormModal({
  isOpen,
  onClose,
  onSave,
  categorias,
  ingredientes,
  initialData,
  isPending = false,
}: ProductFormModalProps) {
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [precio, setPrecio] = useState<number | ''>('')
  const [imagenUrl, setImagenUrl] = useState('')
  const [categoriaIds, setCategoriaIds] = useState<number[]>([])
  const [ingredienteIds, setIngredienteIds] = useState<number[]>([])

  useEffect(() => {
    if (initialData) {
      setNombre(initialData.nombre)
      setDescripcion(initialData.descripcion)
      setPrecio(initialData.precio)
      setImagenUrl(initialData.imagen_url)
      setCategoriaIds(initialData.categoria_ids)
      setIngredienteIds(initialData.ingrediente_ids)
    } else {
      setNombre('')
      setDescripcion('')
      setPrecio('')
      setImagenUrl('')
      setCategoriaIds([])
      setIngredienteIds([])
    }
  }, [initialData, isOpen])

  if (!isOpen) return null

  const isEdit = !!initialData

  const toggleCategoria = (id: number) => {
    setCategoriaIds((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    )
  }

  const toggleIngrediente = (id: number) => {
    setIngredienteIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    )
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nombre.trim() || precio === '' || Number(precio) <= 0) return
    onSave({
      nombre: nombre.trim(),
      descripcion: descripcion.trim(),
      precio: Number(precio),
      imagen_url: imagenUrl.trim(),
      categoria_ids: categoriaIds,
      ingrediente_ids: ingredienteIds,
    })
  }

  const isValid = nombre.trim() && precio !== '' && Number(precio) > 0

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200 sticky top-0 bg-white z-10">
          <h3 className="text-lg font-medium text-gray-900">
            {isEdit ? 'Editar producto' : 'Nuevo producto'}
          </h3>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="px-6 py-4 space-y-4">
            <div>
              <label htmlFor="prod-nombre" className="block text-sm font-medium text-gray-700 mb-1">
                Nombre
              </label>
              <input
                id="prod-nombre"
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Ej: Pizza Margherita"
              />
            </div>

            <div>
              <label htmlFor="prod-desc" className="block text-sm font-medium text-gray-700 mb-1">
                Descripción
              </label>
              <textarea
                id="prod-desc"
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Descripción del producto"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="prod-precio" className="block text-sm font-medium text-gray-700 mb-1">
                  Precio
                </label>
                <input
                  id="prod-precio"
                  type="number"
                  value={precio}
                  onChange={(e) =>
                    setPrecio(e.target.value === '' ? '' : Number(e.target.value))
                  }
                  required
                  min="0.01"
                  step="0.01"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="0.00"
                />
              </div>

              <div>
                <label htmlFor="prod-imagen" className="block text-sm font-medium text-gray-700 mb-1">
                  URL de imagen
                </label>
                <input
                  id="prod-imagen"
                  type="text"
                  value={imagenUrl}
                  onChange={(e) => setImagenUrl(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="https://..."
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Categorías
              </label>
              <div className="max-h-32 overflow-y-auto border border-gray-200 rounded-md p-2 space-y-1">
                {categorias.length === 0 ? (
                  <p className="text-sm text-gray-400 py-2 px-1">No hay categorías disponibles</p>
                ) : (
                  categorias.map((cat) => (
                    <label
                      key={cat.id}
                      className="flex items-center gap-2 px-2 py-1 rounded hover:bg-gray-50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={categoriaIds.includes(cat.id)}
                        onChange={() => toggleCategoria(cat.id)}
                        className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                      />
                      <span className="text-sm text-gray-700">{cat.nombre}</span>
                    </label>
                  ))
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ingredientes
              </label>
              <div className="max-h-32 overflow-y-auto border border-gray-200 rounded-md p-2 space-y-1">
                {ingredientes.length === 0 ? (
                  <p className="text-sm text-gray-400 py-2 px-1">No hay ingredientes disponibles</p>
                ) : (
                  ingredientes.map((ing) => (
                    <label
                      key={ing.id}
                      className="flex items-center gap-2 px-2 py-1 rounded hover:bg-gray-50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={ingredienteIds.includes(ing.id)}
                        onChange={() => toggleIngrediente(ing.id)}
                        className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                      />
                      <span className="text-sm text-gray-700">{ing.nombre}</span>
                      {ing.es_alergeno && (
                        <span className="px-1.5 py-0.5 text-xs font-medium bg-amber-100 text-amber-800 rounded-full">
                          alergeno
                        </span>
                      )}
                    </label>
                  ))
                )}
              </div>
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
              disabled={!isValid || isPending}
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
