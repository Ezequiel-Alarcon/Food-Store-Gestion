import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../../../lib/api'
import { useUIStore } from '../../../stores/uiStore'
import { ProductFormModal } from './ProductFormModal'

interface ProductoAdmin {
  id: number
  nombre: string
  precio: number
  stock: number
  activo: boolean
  categorias: { id: number; nombre: string }[]
  ingredientes: { id: number; nombre: string; es_alergeno: boolean }[]
}

interface ProductFormData {
  nombre: string
  descripcion: string
  precio: number
  imagen_url: string
  categoria_ids: number[]
  ingrediente_ids: number[]
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
  }).format(amount)
}

function TableSkeleton() {
  return (
    <div className="animate-pulse p-6">
      <div className="h-10 bg-gray-200 rounded mb-4" />
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-14 bg-gray-100 rounded mb-2" />
      ))}
    </div>
  )
}

export function ProductsPage() {
  const queryClient = useQueryClient()
  const addToast = useUIStore((s) => s.addToast)
  const openConfirmModal = useUIStore((s) => s.openConfirmModal)

  const [page, setPage] = useState(1)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState<ProductoAdmin | null>(null)

  const { data: allProducts, isLoading: productsLoading, isError: productsError, refetch: refetchProducts } = useQuery({
    queryKey: ['admin-productos'],
    queryFn: async () => {
      const res = await api.get<{ items: ProductoAdmin[] }>('/productos')
      return res.data.items as ProductoAdmin[]
    },
  })

  const { data: categoriasList } = useQuery({
    queryKey: ['categorias-list'],
    queryFn: async () => {
      const res = await api.get('/categorias')
      return res.data as { id: number; nombre: string }[]
    },
    staleTime: 5 * 60 * 1000,
  })

  const { data: ingredientesList } = useQuery({
    queryKey: ['ingredientes-list'],
    queryFn: async () => {
      const res = await api.get('/ingredientes')
      return res.data as { id: number; nombre: string; es_alergeno: boolean }[]
    },
    staleTime: 5 * 60 * 1000,
  })

  const createMutation = useMutation({
    mutationFn: (data: ProductFormData) => api.post('/productos', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-productos'] })
      setModalOpen(false)
      addToast('success', 'Producto creado correctamente')
    },
    onError: (err: unknown) => {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      addToast('error', detail || 'Error al crear el producto')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductFormData }) =>
      api.put(`/productos/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-productos'] })
      setModalOpen(false)
      setEditingProduct(null)
      addToast('success', 'Producto actualizado correctamente')
    },
    onError: (err: unknown) => {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      addToast('error', detail || 'Error al actualizar el producto')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/productos/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-productos'] })
      addToast('success', 'Producto eliminado correctamente')
    },
    onError: (err: unknown) => {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      addToast('error', detail || 'Error al eliminar el producto. Puede estar en pedidos activos.')
    },
  })

  const handleDelete = (product: ProductoAdmin) => {
    openConfirmModal(
      'Eliminar producto',
      `¿Estás seguro de que querés eliminar "${product.nombre}"? Esta acción no se puede deshacer.`,
      () => deleteMutation.mutate(product.id)
    )
  }

  const handleSave = (data: ProductFormData) => {
    if (editingProduct) {
      updateMutation.mutate({ id: editingProduct.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const openCreate = () => {
    setEditingProduct(null)
    setModalOpen(true)
  }

  const openEdit = (product: ProductoAdmin) => {
    setEditingProduct(product)
    setModalOpen(true)
  }

  const products = allProducts || []
  const PAGE_SIZE = 20
  const total = products.length
  const pages = Math.ceil(total / PAGE_SIZE)
  const offset = (page - 1) * PAGE_SIZE
  const paginatedProducts = products.slice(offset, offset + PAGE_SIZE)

  const getInitialFormData = (): ProductFormData | undefined => {
    if (!editingProduct) return undefined
    return {
      nombre: editingProduct.nombre,
      descripcion: '',
      precio: editingProduct.precio,
      imagen_url: '',
      categoria_ids: editingProduct.categorias?.map((c) => c.id) ?? [],
      ingrediente_ids: editingProduct.ingredientes?.map((i) => i.id) ?? [],
    }
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Productos</h1>
          <p className="text-gray-600 mt-1">Gestioná los productos del catálogo</p>
        </div>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
        >
          Nuevo producto
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {productsLoading ? (
          <TableSkeleton />
        ) : productsError ? (
          <div className="p-8 text-center">
            <p className="text-red-600 mb-4">Error al cargar los productos</p>
            <button
              onClick={() => refetchProducts()}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm"
            >
              Reintentar
            </button>
          </div>
        ) : products.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No hay productos</div>
        ) : (
          <>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Precio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stock
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Activo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paginatedProducts.map((product) => (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {product.nombre}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {formatCurrency(product.precio)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${
                          product.stock > 0
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {product.stock}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${
                          product.activo
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {product.activo ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => openEdit(product)}
                        className="text-indigo-600 hover:text-indigo-900 font-medium mr-4"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDelete(product)}
                        disabled={deleteMutation.isPending}
                        className="text-red-600 hover:text-red-900 font-medium disabled:opacity-50"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {pages > 1 && (
              <div className="px-6 py-4 flex items-center justify-between border-t border-gray-200">
                <div className="text-sm text-gray-500">
                  Mostrando {offset + 1}-{Math.min(offset + PAGE_SIZE, total)} de {total} productos
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Anterior
                  </button>
                  <button
                    onClick={() => setPage((p) => Math.min(pages, p + 1))}
                    disabled={page === pages}
                    className="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Siguiente
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {modalOpen && (
        <ProductFormModal
          isOpen={modalOpen}
          onClose={() => {
            setModalOpen(false)
            setEditingProduct(null)
          }}
          onSave={handleSave}
          categorias={categoriasList || []}
          ingredientes={ingredientesList || []}
          initialData={getInitialFormData()}
          isPending={createMutation.isPending || updateMutation.isPending}
        />
      )}
    </div>
  )
}
