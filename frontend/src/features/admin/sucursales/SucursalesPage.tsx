import { useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { useUIStore } from '../../../stores/uiStore'
import {
  useBranches,
  useCreateBranch,
  useUpdateBranch,
  useDeleteBranch,
  useCreateBranchAddress,
  useUpdateBranchAddress,
  useBranchAddresses,
} from '../../../entities/addresses/queries'
import type { Branch, BranchAddress } from '../../../entities/addresses/types'
import { SucursalFormModal } from './SucursalFormModal'

interface SucursalFormData {
  nombre: string
  calle: string
  numero: string
  piso_depto: string
  ciudad: string
  provincia: string
  codigo_postal: string
  pais: string
  referencias: string
}

interface MergedBranch extends Branch {
  direccion: BranchAddress | null
}

function TableSkeleton() {
  return (
    <div className="animate-pulse p-6">
      <div className="h-10 bg-gray-200 rounded mb-4" />
      {[...Array(3)].map((_, i) => (
        <div key={i} className="h-14 bg-gray-100 rounded mb-2" />
      ))}
    </div>
  )
}

function formatAddress(a: BranchAddress): string {
  const parts = [`${a.calle} ${a.numero}`]
  if (a.piso_depto) parts.push(a.piso_depto)
  parts.push(`${a.ciudad}, ${a.provincia}`)
  if (a.codigo_postal) parts.push(`CP ${a.codigo_postal}`)
  return parts.join(' - ')
}

function buildAddressPayload(form: SucursalFormData) {
  return {
    calle: form.calle,
    numero: form.numero,
    piso_depto: form.piso_depto || null,
    ciudad: form.ciudad,
    provincia: form.provincia,
    codigo_postal: form.codigo_postal || null,
    pais: form.pais,
    referencias: form.referencias || null,
  }
}

export function SucursalesPage() {
  const queryClient = useQueryClient()
  const addToast = useUIStore((s) => s.addToast)
  const openConfirmModal = useUIStore((s) => s.openConfirmModal)

  const [modalOpen, setModalOpen] = useState(false)
  const [editingBranch, setEditingBranch] = useState<MergedBranch | null>(null)

  const {
    data: branches = [],
    isLoading: branchesLoading,
    isError: branchesError,
    refetch: refetchBranches,
  } = useBranches()

  const {
    data: addresses = [],
    isLoading: addressesLoading,
  } = useBranchAddresses()

  const createBranchMut = useCreateBranch()
  const updateBranchMut = useUpdateBranch()
  const deleteBranchMut = useDeleteBranch()
  const createAddressMut = useCreateBranchAddress()
  const updateAddressMut = useUpdateBranchAddress()

  // Merge branches with their addresses
  const merged: MergedBranch[] = branches.map((b) => ({
    ...b,
    direccion: addresses.find((a) => a.branch_id === b.id) || null,
  }))

  const isLoading = branchesLoading || addressesLoading

  const handleCreate = async (form: SucursalFormData) => {
    // 1. Create branch
    const branch = await createBranchMut.mutateAsync({ nombre: form.nombre })
    // 2. Create address for the new branch
    await createAddressMut.mutateAsync({
      branchId: branch.id,
      payload: buildAddressPayload(form),
    })
    setModalOpen(false)
    addToast('success', 'Sucursal creada correctamente')
  }

  const handleUpdate = async (form: SucursalFormData) => {
    if (!editingBranch) return
    // 1. Update branch name if changed
    if (form.nombre !== editingBranch.nombre) {
      await updateBranchMut.mutateAsync({ id: editingBranch.id, payload: { nombre: form.nombre } })
    }
    // 2. Update or create address
    if (editingBranch.direccion) {
      await updateAddressMut.mutateAsync({
        branchId: editingBranch.id,
        payload: buildAddressPayload(form),
      })
    } else {
      await createAddressMut.mutateAsync({
        branchId: editingBranch.id,
        payload: buildAddressPayload(form),
      })
    }
    setModalOpen(false)
    setEditingBranch(null)
    addToast('success', 'Sucursal actualizada correctamente')
  }

  const handleDelete = (branch: MergedBranch) => {
    openConfirmModal(
      'Desactivar sucursal',
      `¿Estás seguro de que querés desactivar "${branch.nombre}"? Dejará de aparecer en Puntos de Retiro.`,
      () => {
        deleteBranchMut.mutate(branch.id, {
          onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['branches'] })
            addToast('success', `Sucursal "${branch.nombre}" desactivada`)
          },
          onError: (err: unknown) => {
            const detail =
              (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
            addToast('error', detail || 'Error al desactivar la sucursal')
          },
        })
      }
    )
  }

  const openCreate = () => {
    setEditingBranch(null)
    setModalOpen(true)
  }

  const openEdit = (branch: MergedBranch) => {
    setEditingBranch(branch)
    setModalOpen(true)
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Sucursales</h1>
          <p className="text-gray-600 mt-1">Gestioná las sucursales y puntos de retiro</p>
        </div>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
        >
          Nueva sucursal
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {isLoading ? (
          <TableSkeleton />
        ) : branchesError ? (
          <div className="p-8 text-center">
            <p className="text-red-600 mb-4">Error al cargar las sucursales</p>
            <button
              onClick={() => refetchBranches()}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm"
            >
              Reintentar
            </button>
          </div>
        ) : merged.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            No hay sucursales. Creá la primera.
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Dirección
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
              {merged.map((branch) => (
                <tr key={branch.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {branch.nombre}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                    {branch.direccion ? formatAddress(branch.direccion) : 'Sin dirección'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        branch.activa
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {branch.activa ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => openEdit(branch)}
                      className="text-indigo-600 hover:text-indigo-900 font-medium mr-4"
                    >
                      Editar
                    </button>
                    {branch.activa && (
                      <button
                        onClick={() => handleDelete(branch)}
                        disabled={deleteBranchMut.isPending}
                        className="text-red-600 hover:text-red-900 font-medium disabled:opacity-50"
                      >
                        Desactivar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modalOpen && (
        <SucursalFormModal
          isOpen={modalOpen}
          onClose={() => {
            setModalOpen(false)
            setEditingBranch(null)
          }}
          onSave={editingBranch ? handleUpdate : handleCreate}
          initialData={
            editingBranch
              ? { branch: editingBranch, address: editingBranch.direccion }
              : undefined
          }
          isPending={
            createBranchMut.isPending ||
            updateBranchMut.isPending ||
            createAddressMut.isPending ||
            updateAddressMut.isPending
          }
        />
      )}
    </div>
  )
}
