import { api } from '../../lib/api'
import type {
  UserAddress,
  UserAddressCreate,
  UserAddressUpdate,
  BranchAddress,
  BranchAddressCreate,
  BranchAddressUpdate,
} from './types'

export const userAddressesApi = {
  list: async (): Promise<UserAddress[]> => {
    const res = await api.get<UserAddress[]>('/user/addresses')
    return res.data
  },
  create: async (payload: UserAddressCreate): Promise<UserAddress> => {
    const res = await api.post<UserAddress>('/user/addresses', payload)
    return res.data
  },
  update: async (id: number, payload: UserAddressUpdate): Promise<UserAddress> => {
    const res = await api.patch<UserAddress>(`/user/addresses/${id}`, payload)
    return res.data
  },
  remove: async (id: number): Promise<void> => {
    await api.delete(`/user/addresses/${id}`)
  },
  setDefault: async (id: number): Promise<UserAddress> => {
    const res = await api.post<UserAddress>(`/user/addresses/${id}/default`)
    return res.data
  },
}

export const branchAddressesApi = {
  list: async (): Promise<BranchAddress[]> => {
    const res = await api.get<BranchAddress[]>('/branches/addresses')
    return res.data
  },
  create: async (branchId: number, payload: BranchAddressCreate): Promise<BranchAddress> => {
    const res = await api.post<BranchAddress>(`/branches/${branchId}/address`, payload)
    return res.data
  },
  update: async (branchId: number, payload: BranchAddressUpdate): Promise<BranchAddress> => {
    const res = await api.patch<BranchAddress>(`/branches/${branchId}/address`, payload)
    return res.data
  },
  remove: async (branchId: number): Promise<void> => {
    await api.delete(`/branches/${branchId}/address`)
  },
}
