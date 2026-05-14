import { useState } from 'react'

interface IngredientItem {
  id: number
  nombre: string
}

interface IngredientsModalProps {
  productName: string
  ingredients: IngredientItem[]
  onConfirm: (excludedIds: number[]) => void
  onClose: () => void
}

export function IngredientsModal({
  productName,
  ingredients,
  onConfirm,
  onClose,
}: IngredientsModalProps) {
  const [excluded, setExcluded] = useState<Set<number>>(new Set())

  const toggleIngredient = (id: number) => {
    setExcluded((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />

      {/* Modal */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          Personalizar: {productName}
        </h2>
        <p className="text-sm text-gray-500 mb-4">
          Desmarcá los ingredientes que querés excluir:
        </p>

        {ingredients.length === 0 ? (
          <p className="text-sm text-gray-400 py-2">
            Este producto no tiene ingredientes configurables.
          </p>
        ) : (
          <div className="space-y-2 max-h-64 overflow-y-auto mb-4">
            {ingredients.map((ing) => (
              <label
                key={ing.id}
                className="flex items-center gap-3 p-2 rounded hover:bg-gray-50 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={!excluded.has(ing.id)}
                  onChange={() => toggleIngredient(ing.id)}
                  className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                />
                <span
                  className={`text-sm ${
                    excluded.has(ing.id)
                      ? 'text-gray-400 line-through'
                      : 'text-gray-700'
                  }`}
                >
                  {ing.nombre}
                </span>
              </label>
            ))}
          </div>
        )}

        <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
          >
            Cancelar
          </button>
          <button
            onClick={() => onConfirm(Array.from(excluded))}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Agregar al carrito
          </button>
        </div>
      </div>
    </div>
  )
}
