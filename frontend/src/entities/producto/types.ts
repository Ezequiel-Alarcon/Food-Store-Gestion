/**
 * frontend/src/entities/producto/types.ts
 *
 * Tipos TypeScript para el módulo de productos.
 */

export interface CategoriaSimple {
  id: number
  nombre: string
}

export interface IngredienteSimple {
  id: number
  nombre: string
  es_alergeno: boolean
}

/** Respuesta del catálogo público (lista) */
export interface ProductoCatalogo {
  id: number
  nombre: string
  descripcion: string | null
  precio: number
  imagen_url: string | null
  disponible: boolean
  categorias: CategoriaSimple[]
}

/** Respuesta de detalle público (incluye ingredientes, sin stock exacto) */
export interface ProductoDetalle {
  id: number
  nombre: string
  descripcion: string | null
  precio: number
  imagen_url: string | null
  disponible: boolean
  categorias: CategoriaSimple[]
  ingredientes: IngredienteSimple[]
}

/** Respuesta paginada del backend */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
