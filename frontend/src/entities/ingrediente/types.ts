/**
 * frontend/src/entities/ingrediente/types.ts
 *
 * Tipos TypeScript para el módulo de ingredientes.
 */

export interface IngredienteResponse {
  id: number
  nombre: string
  descripcion: string | null
  es_alergeno: boolean
  creado_en: string
  actualizado_en: string | null
}

export interface IngredienteCreate {
  nombre: string
  descripcion?: string | null
  es_alergeno?: boolean
}

export interface IngredienteUpdate {
  nombre?: string
  descripcion?: string | null
  es_alergeno?: boolean
}

export interface IngredienteListResponse {
  id: number
  nombre: string
  descripcion: string | null
  es_alergeno: boolean
  creado_en: string
  actualizado_en: string | null
}