import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { branchAddressesApi, userAddressesApi } from './api'
import type { UserAddressCreate, UserAddressUpdate } from './types'

const keys = {
  userAddresses: ['user-addresses'] as const,
  branchAddresses: ['branch-addresses'] as const,
}

export function useUserAddresses() {
  return useQuery({
    queryKey: keys.userAddresses,
    queryFn: userAddressesApi.list,
  })
}

export function useCreateUserAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: UserAddressCreate) => userAddressesApi.create(payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.userAddresses })
    },
  })
}

export function useUpdateUserAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UserAddressUpdate }) =>
      userAddressesApi.update(id, payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.userAddresses })
    },
  })
}

export function useDeleteUserAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => userAddressesApi.remove(id),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.userAddresses })
    },
  })
}

export function useSetDefaultUserAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => userAddressesApi.setDefault(id),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.userAddresses })
    },
  })
}

export function useBranchAddresses() {
  return useQuery({
    queryKey: keys.branchAddresses,
    queryFn: branchAddressesApi.list,
  })
}
