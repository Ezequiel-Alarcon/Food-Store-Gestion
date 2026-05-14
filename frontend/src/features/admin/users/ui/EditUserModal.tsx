import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { usuarioAdminApi } from '../../../../entities/usuario-admin/api'
import { ROLES } from '../../../../entities/usuario-admin/types'
import type { UserAdmin, RolValue } from '../../../../entities/usuario-admin/types'

interface EditUserModalProps {
  user: UserAdmin
  onClose: () => void
  onSuccess: () => void
  currentUserId: number | undefined
}

export function EditUserModal({ user, onClose, onSuccess, currentUserId }: EditUserModalProps) {
  const [selectedRole, setSelectedRole] = useState<RolValue>(user.rol as RolValue)
  const [showLastAdminWarning, setShowLastAdminWarning] = useState(false)
  const queryClient = useQueryClient()

  const isSelf = user.id === currentUserId
  const isLastAdmin =
    user.rol === 'ADMIN' && selectedRole !== 'ADMIN' && !showLastAdminWarning

  const updateMutation = useMutation({
    mutationFn: (rol: string) => usuarioAdminApi.updateUser(user.id, { rol }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      onSuccess()
      onClose()
    },
    onError: () => {
      alert('Error al actualizar el usuario')
    },
  })

  const handleSave = () => {
    if (user.rol === 'ADMIN' && selectedRole !== 'ADMIN') {
      setShowLastAdminWarning(true)
      return
    }
    updateMutation.mutate(selectedRole)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Editar Usuario</h3>
        </div>

        <div className="px-6 py-4 space-y-4">
          <div>
            <p className="text-sm text-gray-600">
              <strong>{user.nombre} {user.apellido}</strong> ({user.email})
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Rol</label>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value as RolValue)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              {ROLES.map((rol) => (
                <option key={rol} value={rol}>
                  {rol}
                </option>
              ))}
            </select>
          </div>

          {showLastAdminWarning && (
            <div className="bg-amber-50 border border-amber-200 rounded p-3">
              <p className="text-sm text-amber-800">
                ⚠️ Este usuario es el último administrador del sistema. ¿Estás seguro de que
                quieres quitarle el rol ADMIN?
              </p>
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => {
                    setShowLastAdminWarning(false)
                    updateMutation.mutate(selectedRole)
                  }}
                  className="px-3 py-1 bg-amber-600 text-white text-sm rounded hover:bg-amber-700"
                >
                  Sí, continuar
                </button>
                <button
                  onClick={() => setShowLastAdminWarning(false)}
                  className="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300"
                >
                  Cancelar
                </button>
              </div>
            </div>
          )}

          {isSelf && selectedRole !== 'ADMIN' && !showLastAdminWarning && (
            <p className="text-sm text-amber-600">
              ⚠️ Estás a punto de cambiar tu propio rol. Necesitarás volver a iniciar sesión.
            </p>
          )}
        </div>

        <div className="px-6 py-4 bg-gray-50 flex justify-end gap-3 rounded-b-lg">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-100"
          >
            Cancelar
          </button>
          <button
            onClick={handleSave}
            disabled={updateMutation.isPending}
            className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700 disabled:opacity-50"
          >
            {updateMutation.isPending ? 'Guardando...' : 'Guardar'}
          </button>
        </div>
      </div>
    </div>
  )
}