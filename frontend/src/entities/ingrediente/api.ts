/**
 * frontend/src/entities/ingrediente/api.ts
 *
 * Cliente API para el módulo de ingredientes.
 */

import { api } from '../../lib/api'
import type {
  IngredienteResponse,
  IngredienteCreate,
  IngredienteUpdate,
} from './types'

export interface GetAllParams {
  skip?: number
  limit?: number
  es_alergeno?: boolean | null
}

export const ingredienteApi = {
  /**
   * Obtiene todos los ingredientes con paginación y filtro opcional.
   */
  getAll: async (params?: GetAllParams): Promise<IngredienteResponse[]> => {
    const searchParams = new URLSearchParams()
    if (params?.skip !== undefined) searchParams.set('skip', String(params.skip))
    if (params?.limit !== undefined) searchParams.set('limit', String(params.limit))
    if (params?.es_alergeno !== undefined && params.es_alergeno !== null) {
      searchParams.set('es_alergeno', String(params.es_alergeno))
    }
    const query = searchParams.toString()
    const url = `/ingredientes${query ? `?${query}` : ''}`
    const response = await api.get<IngredienteResponse[]>(url)
    return response.data
  },

  /**
   * Obtiene un ingrediente por ID.
   */
  getById: async (id: number): Promise<IngredienteResponse> => {
    const response = await api.get<IngredienteResponse>(`/ingredientes/${id}`)
    return response.data
  },

  /**
   * Crea un nuevo ingrediente.
   */
  create: async (data: IngredienteCreate): Promise<IngredienteResponse> => {
    const response = await api.post<IngredienteResponse>('/ingredientes/', data)
    return response.data
  },

  /**
   * Actualiza un ingrediente (PATCH - parcial).
   */
  update: async (id: number, data: IngredienteUpdate): Promise<IngredienteResponse> => {
    const response = await api.patch<IngredienteResponse>(`/ingredientes/${id}`, data)
    return response.data
  },

  /**
   * Elimina un ingrediente (soft-delete).
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/ingredientes/${id}`)
  },
}