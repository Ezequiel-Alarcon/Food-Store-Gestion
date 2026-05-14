import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuthStore } from '../../../../stores/authStore'
import { usuarioAdminApi } from '../../../../entities/usuario-admin/api'
import { SearchInput } from './SearchInput'
import { RoleFilter } from './RoleFilter'
import { EditUserModal } from './EditUserModal'
import type { UserAdmin } from '../../../../entities/usuario-admin/types'

const ROL_COLORS: Record<string, string> = {
  ADMIN: 'bg-red-100 text-red-800',
  STOCK: 'bg-orange-100 text-orange-800',
  PEDIDOS: 'bg-blue-100 text-blue-800',
  CLIENT: 'bg-green-100 text-green-800',
}

function formatDate(dateString: string | null): string {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
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

export function UsersPage() {
  const [page] = useState(1)
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [editingUser, setEditingUser] = useState<UserAdmin | null>(null)
  const [confirmToggle, setConfirmToggle] = useState<UserAdmin | null>(null)

  const currentUser = useAuthStore((state) => state.user)
  const queryClient = useQueryClient()

  const { data: allUsers, isLoading, isError, refetch } = useQuery({
    queryKey: ['admin-users'],
    queryFn: () => usuarioAdminApi.listUsers(true),
  })

  const toggleMutation = useMutation({
    mutationFn: async (user: UserAdmin) => {
      if (user.activo) {
        await usuarioAdminApi.deactivateUser(user.id)
      } else {
        await usuarioAdminApi.activateUser(user.id)
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      setConfirmToggle(null)
    },
    onError: () => {
      alert('Error al cambiar el estado del usuario')
    },
  })

  // Filtrado en frontend (backend no soporta filtros)
  const filteredUsers = (allUsers || []).filter((user) => {
    const matchesSearch =
      !search ||
      user.nombre.toLowerCase().includes(search.toLowerCase()) ||
      user.apellido.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase())
    const matchesRole = !roleFilter || user.rol === roleFilter
    return matchesSearch && matchesRole
  })

  // Paginación simple
  const PAGE_SIZE = 20
  const total = filteredUsers.length
  const pages = Math.ceil(total / PAGE_SIZE)
  const offset = (page - 1) * PAGE_SIZE
  const paginatedUsers = filteredUsers.slice(offset, offset + PAGE_SIZE)

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
        <p className="text-gray-600 mt-1">Administra todos los usuarios del sistema</p>
      </div>

      {/* Filtros */}
      <div className="flex flex-wrap gap-4 mb-6">
        <div className="flex-1 min-w-[200px] max-w-md">
          <SearchInput value={search} onChange={setSearch} placeholder="Buscar por nombre o email..." />
        </div>
        <div className="w-48">
          <RoleFilter value={roleFilter} onChange={setRoleFilter} />
        </div>
      </div>

      {/* Tabla */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {isLoading ? (
          <div className="p-6"><TableSkeleton /></div>
        ) : isError ? (
          <div className="p-8 text-center">
            <p className="text-red-600 mb-4">Error al cargar los usuarios</p>
            <button
              onClick={() => refetch()}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            >
              Reintentar
            </button>
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No se encontraron usuarios</div>
        ) : (
          <>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rol</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha de Registro</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paginatedUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {user.nombre} {user.apellido}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{user.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${ROL_COLORS[user.rol] || 'bg-gray-100 text-gray-800'}`}>
                        {user.rol}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${user.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {user.activo ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{formatDate(user.created_at)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => setEditingUser(user)}
                        className="text-indigo-600 hover:text-indigo-900 text-sm font-medium mr-4"
                      >
                        Editar
                      </button>
                      {user.id !== currentUser?.id && (
                        <button
                          onClick={() => setConfirmToggle(user)}
                          className={`text-sm font-medium ${user.activo ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'}`}
                        >
                          {user.activo ? 'Desactivar' : 'Activar'}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Paginación */}
            {pages > 1 && (
              <div className="px-6 py-4 flex items-center justify-between border-t border-gray-200">
                <div className="text-sm text-gray-500">
                  Mostrando {offset + 1}-{Math.min(offset + PAGE_SIZE, total)} de {total} usuarios
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    disabled={page === 1}
                    className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                  >
                    Anterior
                  </button>
                  <button
                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    disabled={page === pages}
                    className="px-3 py-1 border rounded text-sm disabled:opacity-50"
                  >
                    Siguiente
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modal de edición */}
      {editingUser && (
        <EditUserModal
          user={editingUser}
          onClose={() => setEditingUser(null)}
          onSuccess={() => {}}
          currentUserId={currentUser?.id}
        />
      )}

      {/* Modal de confirmación toggle */}
      {confirmToggle && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-sm w-full mx-4 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {confirmToggle.activo ? 'Desactivar usuario' : 'Activar usuario'}
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              ¿Estás seguro de que quieres {confirmToggle.activo ? 'desactivar' : 'activar'} a{' '}
              <strong>{confirmToggle.nombre} {confirmToggle.apellido}</strong>?
            </p>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setConfirmToggle(null)}
                className="px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-100"
              >
                Cancelar
              </button>
                <button
                  onClick={() => toggleMutation.mutate(confirmToggle)}
                  disabled={toggleMutation.isPending}
                  className={`px-4 py-2 text-white rounded text-sm ${confirmToggle.activo ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'} disabled:opacity-50`}
                >
                {toggleMutation.isPending ? 'Procesando...' : 'Confirmar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}