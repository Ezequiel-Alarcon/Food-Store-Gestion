import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../../../lib/api'
import { useUIStore } from '../../../stores/uiStore'
import { CategoriesModal } from './CategoriesModal'

interface Categoria {
  id: number
  nombre: string
  categoria_padre_id: number | null
  nivel?: number
  activa: boolean
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

export function CategoriesPage() {
  const queryClient = useQueryClient()
  const addToast = useUIStore((s) => s.addToast)
  const openConfirmModal = useUIStore((s) => s.openConfirmModal)

  const [modalOpen, setModalOpen] = useState(false)
  const [editingCat, setEditingCat] = useState<Categoria | null>(null)

  const {
    data: categorias,
    isLoading,
    isError,
    refetch,
  } = useQuery({
    queryKey: ['admin-categorias'],
    queryFn: async () => {
      const res = await api.get('/categorias?tree=true')
      return res.data as Categoria[]
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: { nombre: string; categoria_padre_id: number | null }) =>
      api.post('/categorias', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-categorias'] })
      setModalOpen(false)
      addToast('success', 'Categoría creada correctamente')
    },
    onError: () => {
      addToast('error', 'Error al crear la categoría')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number
      data: { nombre: string; categoria_padre_id: number | null }
    }) => api.put(`/categorias/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-categorias'] })
      setModalOpen(false)
      setEditingCat(null)
      addToast('success', 'Categoría actualizada correctamente')
    },
    onError: () => {
      addToast('error', 'Error al actualizar la categoría')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/categorias/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-categorias'] })
      addToast('success', 'Categoría eliminada correctamente')
    },
    onError: () => {
      addToast('error', 'Error al eliminar la categoría. Puede tener productos asociados.')
    },
  })

  const handleDelete = (cat: Categoria) => {
    openConfirmModal(
      'Eliminar categoría',
      `¿Estás seguro de que querés eliminar "${cat.nombre}"? Esta acción no se puede deshacer.`,
      () => deleteMutation.mutate(cat.id)
    )
  }

  const handleSave = (data: { nombre: string; categoria_padre_id: number | null }) => {
    if (editingCat) {
      updateMutation.mutate({ id: editingCat.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const openCreate = () => {
    setEditingCat(null)
    setModalOpen(true)
  }

  const openEdit = (cat: Categoria) => {
    setEditingCat(cat)
    setModalOpen(true)
  }

  const getParentName = (parentId: number | null) => {
    if (parentId === null) return '—'
    const parent = categorias?.find((c) => c.id === parentId)
    return parent?.nombre || `#${parentId}`
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Categorías</h1>
          <p className="text-gray-600 mt-1">Gestioná las categorías del catálogo</p>
        </div>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
        >
          Nueva categoría
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {isLoading ? (
          <TableSkeleton />
        ) : isError ? (
          <div className="p-8 text-center">
            <p className="text-red-600 mb-4">Error al cargar las categorías</p>
            <button
              onClick={() => refetch()}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm"
            >
              Reintentar
            </button>
          </div>
        ) : !categorias || categorias.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No hay categorías</div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoría Padre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {categorias.map((cat) => (
                <tr key={cat.id} className="hover:bg-gray-50">
                  <td
                    className="px-6 py-4 text-sm font-medium text-gray-900"
                    style={{ paddingLeft: `${(cat.nivel ?? 0) * 20 + 24}px` }}
                  >
                    {cat.nombre}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {getParentName(cat.categoria_padre_id)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        cat.activa
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {cat.activa ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => openEdit(cat)}
                      className="text-indigo-600 hover:text-indigo-900 font-medium mr-4"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(cat)}
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
        )}
      </div>

      {modalOpen && (
        <CategoriesModal
          isOpen={modalOpen}
          onClose={() => {
            setModalOpen(false)
            setEditingCat(null)
          }}
          onSave={handleSave}
          categorias={categorias || []}
          initialData={
            editingCat
              ? { nombre: editingCat.nombre, categoria_padre_id: editingCat.categoria_padre_id }
              : undefined
          }
          isPending={createMutation.isPending || updateMutation.isPending}
        />
      )}
    </div>
  )
}
