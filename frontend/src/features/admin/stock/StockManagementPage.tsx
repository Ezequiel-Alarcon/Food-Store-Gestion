import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../../../lib/api'
import { useUIStore } from '../../../stores/uiStore'

interface ProductoAdmin {
  id: number
  nombre: string
  stock: number
  activo: boolean
  precio: number
}

interface ProductoRowState {
  stock: number
  activo: boolean
}

function TableSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-10 bg-gray-200 rounded mb-4" />
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-16 bg-gray-100 rounded mb-2" />
      ))}
    </div>
  )
}

export function StockManagementPage() {
  const addToast = useUIStore((s) => s.addToast)
  const queryClient = useQueryClient()
  const [page, setPage] = useState(1)
  const [rowStates, setRowStates] = useState<Record<number, ProductoRowState>>({})
  const PAGE_SIZE = 15

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['admin-productos'],
    queryFn: async (): Promise<ProductoAdmin[]> => {
      const response = await api.get<ProductoAdmin[]>('/productos')
      return response.data
    },
  })

  const updateMutation = useMutation({
    mutationFn: async ({
      id,
      stock,
      activo,
    }: {
      id: number
      stock: number
      activo: boolean
    }) => {
      await api.patch(`/productos/${id}/stock`, { stock, activo })
    },
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['admin-productos'] })
      addToast('success', `Producto #${variables.id} actualizado correctamente`)
    },
    onError: (err: unknown, variables) => {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      addToast('error', detail || `Error al actualizar producto #${variables.id}`)
    },
  })

  const allProducts = data || []
  const total = allProducts.length
  const pages = Math.ceil(total / PAGE_SIZE)
  const offset = (page - 1) * PAGE_SIZE
  const paginatedProducts = allProducts.slice(offset, offset + PAGE_SIZE)

  function initRow(product: ProductoAdmin) {
    if (rowStates[product.id] === undefined) {
      setRowStates((prev) => ({
        ...prev,
        [product.id]: { stock: product.stock, activo: product.activo },
      }))
    }
  }

  function getRowState(product: ProductoAdmin): ProductoRowState {
    return rowStates[product.id] ?? { stock: product.stock, activo: product.activo }
  }

  function updateRow(productId: number, field: keyof ProductoRowState, value: number | boolean) {
    setRowStates((prev) => ({
      ...prev,
      [productId]: { ...prev[productId], [field]: value },
    }))
  }

  function handleSave(product: ProductoAdmin) {
    const row = getRowState(product)
    updateMutation.mutate({ id: product.id, stock: row.stock, activo: row.activo })
  }

  function hasChanges(product: ProductoAdmin): boolean {
    const row = getRowState(product)
    return row.stock !== product.stock || row.activo !== product.activo
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Gestión de Stock</h1>
        <p className="text-gray-600 mt-1">Administración de inventario</p>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {isLoading ? (
          <div className="p-6"><TableSkeleton /></div>
        ) : isError ? (
          <div className="p-8 text-center">
            <p className="text-red-600 mb-4">Error al cargar los productos</p>
            <button
              onClick={() => refetch()}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
            >
              Reintentar
            </button>
          </div>
        ) : allProducts.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            No se encontraron productos
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Nombre
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Stock actual
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Nuevo stock
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Activo
                    </th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acción
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {paginatedProducts.map((product) => {
                    initRow(product)
                    const row = getRowState(product)
                    return (
                      <tr key={product.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">
                          {product.nombre}
                        </td>
                        <td className="px-6 py-4 text-center text-sm text-gray-500">
                          {product.stock}
                        </td>
                        <td className="px-6 py-4 text-center">
                          <input
                            type="number"
                            min={0}
                            className="w-24 border border-gray-300 rounded px-2 py-1 text-sm text-center"
                            value={row.stock}
                            onChange={(e) =>
                              updateRow(product.id, 'stock', Math.max(0, Number(e.target.value)))
                            }
                          />
                        </td>
                        <td className="px-6 py-4 text-center">
                          <button
                            type="button"
                            onClick={() => updateRow(product.id, 'activo', !row.activo)}
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              row.activo ? 'bg-green-600' : 'bg-gray-300'
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                row.activo ? 'translate-x-6' : 'translate-x-1'
                              }`}
                            />
                          </button>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <button
                            type="button"
                            onClick={() => handleSave(product)}
                            disabled={
                              !hasChanges(product) || updateMutation.isPending
                            }
                            className="px-4 py-1 bg-indigo-600 text-white rounded text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {updateMutation.isPending &&
                            updateMutation.variables?.id === product.id
                              ? 'Guardando...'
                              : 'Guardar'}
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>

            {pages > 1 && (
              <div className="px-6 py-4 flex items-center justify-between border-t border-gray-200">
                <div className="text-sm text-gray-500">
                  Mostrando {offset + 1}-{Math.min(offset + PAGE_SIZE, total)} de {total} productos
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                  >
                    Anterior
                  </button>
                  <button
                    type="button"
                    onClick={() => setPage((p) => Math.min(pages, p + 1))}
                    disabled={page === pages}
                    className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                  >
                    Siguiente
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
