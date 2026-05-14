import { api } from '../../lib/api'
import type { UserAdmin, UserUpdatePayload } from './types'

export const usuarioAdminApi = {
  /** Listar todos los usuarios */
  listUsers: async (includeInactive = false): Promise<UserAdmin[]> => {
    const params = new URLSearchParams()
    if (includeInactive) params.set('include_inactive', 'true')
    const query = params.toString() ? '?' + params.toString() : ''
    const response = await api.get<UserAdmin[]>(`/usuarios${query}`)
    return response.data
  },

  /** Obtener un usuario por ID */
  getUserById: async (id: number): Promise<UserAdmin> => {
    const response = await api.get<UserAdmin>(`/usuarios/${id}`)
    return response.data
  },

  /** Actualizar datos de usuario (backend usa Query params) */
  updateUser: async (id: number, payload: UserUpdatePayload): Promise<UserAdmin> => {
    const params = new URLSearchParams()
    if (payload.nombre !== undefined) params.set('nombre', payload.nombre)
    if (payload.apellido !== undefined) params.set('apellido', payload.apellido)
    if (payload.rol !== undefined) params.set('rol', payload.rol)
    if (payload.telefono !== undefined) params.set('telefono', payload.telefono)
    if (payload.activo !== undefined) params.set('activo', String(payload.activo))

    const response = await api.put<UserAdmin>(`/usuarios/${id}?${params.toString()}`)
    return response.data
  },

  /** Desactivar usuario (backend usa DELETE, no PATCH) */
  deactivateUser: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/usuarios/${id}`)
    return response.data
  },

  /** Activar usuario — PUT con activo: true */
  activateUser: async (id: number): Promise<UserAdmin> => {
    const response = await api.put<UserAdmin>(`/usuarios/${id}?activo=true`)
    return response.data
  },
}