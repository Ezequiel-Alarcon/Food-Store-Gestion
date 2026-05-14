import { api } from '../../lib/api'
import type { PedidoListItem, PedidoDetalle, PaginatedPedidos } from './types'

export interface PedidoFilters {
  page?: number
  size?: number
  estado?: string
}

export const pedidoApi = {
  getMisPedidos: async (filters?: PedidoFilters): Promise<PaginatedPedidos> => {
    const params = new URLSearchParams()
    if (filters?.page) params.set('page', String(filters.page))
    if (filters?.size) params.set('size', String(filters.size))
    if (filters?.estado) params.set('estado', filters.estado)
    const q = params.toString()
    const response = await api.get<PaginatedPedidos>(`/pedidos${q ? `?${q}` : ''}`)
    return response.data
  },

  getById: async (id: number): Promise<PedidoDetalle> => {
    const response = await api.get<PedidoDetalle>(`/pedidos/${id}`)
    return response.data
  },
}
