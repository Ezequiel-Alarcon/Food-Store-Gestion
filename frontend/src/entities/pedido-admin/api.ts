import { api } from '../../lib/api'
import type {
  OrderAdminDetail,
  OrderAdminFilters,
  PaginatedOrdersAdmin,
  OrderHistoryItem,
} from './types'

export const pedidoAdminApi = {
  /** Listar pedidos con filtros (endpoint admin) */
  listOrders: async (filters?: OrderAdminFilters): Promise<PaginatedOrdersAdmin> => {
    const params = new URLSearchParams()
    if (filters?.page) params.set('page', String(filters.page))
    if (filters?.size) params.set('size', String(filters.size))
    if (filters?.estado) params.set('estado', filters.estado)
    if (filters?.q) params.set('q', filters.q)
    if (filters?.desde) params.set('desde', filters.desde)
    if (filters?.hasta) params.set('hasta', filters.hasta)

    const queryString = params.toString()
    const response = await api.get<PaginatedOrdersAdmin>(
      `/admin/pedidos${queryString ? `?${queryString}` : ''}`
    )
    return response.data
  },

  /** Obtener detalle de un pedido (endpoint admin) */
  getOrderById: async (id: number): Promise<OrderAdminDetail> => {
    const response = await api.get<OrderAdminDetail>(`/admin/pedidos/${id}`)
    return response.data
  },

  /** Obtener historial de estados de un pedido */
  getOrderHistory: async (id: number): Promise<OrderHistoryItem[]> => {
    const response = await api.get<OrderHistoryItem[]>(`/admin/pedidos/${id}/historial`)
    return response.data
  },
}