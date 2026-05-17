import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { perfilApi } from './api'
import type { PerfilResponse, UpdateProfileRequest, ChangePasswordRequest, MessageResponse } from './types'
import { useAuthStore } from '../../stores/authStore'

export function usePerfil() {
  return useQuery<PerfilResponse>({
    queryKey: ['perfil'],
    queryFn: perfilApi.getPerfil,
    staleTime: 0,
  })
}

export function useUpdatePerfil() {
  const qc = useQueryClient()
  return useMutation<PerfilResponse, Error, UpdateProfileRequest>({
    mutationFn: (payload) => perfilApi.updatePerfil(payload),
    onSuccess: async (data) => {
      await qc.invalidateQueries({ queryKey: ['perfil'] })
      useAuthStore.getState().setUser({
        id: data.id,
        nombre: data.nombre,
        email: data.email,
        roles: [data.rol],
      })
    },
  })
}

export function useChangePassword() {
  return useMutation<MessageResponse, Error, ChangePasswordRequest>({
    mutationFn: (payload) => perfilApi.changePassword(payload),
  })
}
