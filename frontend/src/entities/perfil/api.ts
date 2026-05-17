import { api } from '../../lib/api'
import type { PerfilResponse, UpdateProfileRequest, ChangePasswordRequest, MessageResponse } from './types'

export const perfilApi = {
  getPerfil: async (): Promise<PerfilResponse> => {
    const response = await api.get<PerfilResponse>('/perfil')
    return response.data
  },

  updatePerfil: async (payload: UpdateProfileRequest): Promise<PerfilResponse> => {
    const response = await api.put<PerfilResponse>('/perfil', payload)
    return response.data
  },

  changePassword: async (payload: ChangePasswordRequest): Promise<MessageResponse> => {
    const response = await api.put<MessageResponse>('/perfil/password', payload)
    return response.data
  },
}
