import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { branchAddressesApi, branchesApi, userAddressesApi } from './api'
import type {
  BranchAddressCreate,
  BranchAddressUpdate,
  BranchCreate,
  BranchUpdate,
  UserAddressCreate,
  UserAddressUpdate,
} from './types'

const keys = {
  userAddresses: ['user-addresses'] as const,
  branchAddresses: ['branch-addresses'] as const,
  branches: ['branches'] as const,
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

// --- Branch (Sucursales) ---

export function useBranches() {
  return useQuery({
    queryKey: keys.branches,
    queryFn: branchesApi.list,
  })
}

export function useCreateBranch() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: BranchCreate) => branchesApi.create(payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branches })
    },
  })
}

export function useUpdateBranch() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: BranchUpdate }) =>
      branchesApi.update(id, payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branches })
    },
  })
}

export function useDeleteBranch() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => branchesApi.remove(id),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branches })
    },
  })
}

// --- Branch Address mutations ---

export function useCreateBranchAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ branchId, payload }: { branchId: number; payload: BranchAddressCreate }) =>
      branchAddressesApi.create(branchId, payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branchAddresses })
    },
  })
}

export function useUpdateBranchAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({
      branchId,
      payload,
    }: {
      branchId: number
      payload: BranchAddressUpdate
    }) => branchAddressesApi.update(branchId, payload),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branchAddresses })
    },
  })
}

export function useDeleteBranchAddress() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (branchId: number) => branchAddressesApi.remove(branchId),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: keys.branchAddresses })
    },
  })
}
