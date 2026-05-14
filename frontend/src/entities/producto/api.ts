/**
 * frontend/src/entities/producto/api.ts
 *
 * Cliente API para el módulo de productos — solo endpoints públicos del catálogo.
 */

import { api } from '../../lib/api'
import type { ProductoCatalogo, ProductoDetalle, PaginatedResponse } from './types'

export interface CatalogoParams {
  /** ID de categoría para filtrar */
  categoria_id?: number
  /** Solo productos con stock disponible */
  disponibles?: boolean
  /** Número de página (1-based) */
  page?: number
  /** Items por página */
  size?: number
}

export const productoApi = {
  /**
   * Obtiene productos del catálogo público con filtros y paginación.
   * GET /api/v1/productos/catalogo
   */
  getCatalogo: async (params?: CatalogoParams): Promise<PaginatedResponse<ProductoCatalogo>> => {
    const searchParams = new URLSearchParams()
    if (params?.categoria_id !== undefined) searchParams.set('categoria_id', String(params.categoria_id))
    if (params?.disponibles !== undefined) searchParams.set('disponibles', String(params.disponibles))
    // Convertir page-based a offset-based: skip = (page - 1) * size
    const size = params?.size ?? 20
    const page = params?.page ?? 1
    searchParams.set('skip', String((page - 1) * size))
    searchParams.set('limit', String(size))
    const query = searchParams.toString()
    const url = `/productos/catalogo${query ? `?${query}` : ''}`
    const response = await api.get<PaginatedResponse<ProductoCatalogo>>(url)
    return response.data
  },

  /**
   * Obtiene el detalle público de un producto (sin stock exacto, con ingredientes).
   * GET /api/v1/productos/{id}/publico
   */
  getById: async (id: number): Promise<ProductoDetalle> => {
    const response = await api.get<ProductoDetalle>(`/productos/${id}/publico`)
    return response.data
  },
}
