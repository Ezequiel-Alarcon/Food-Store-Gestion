/** Tipos para el módulo de pedidos (vista cliente) */

export interface DetalleItem {
  id: number
  producto_id: number
  cantidad: number
  precio_unitario: number
  exclusiones: number[]
}

export interface PedidoListItem {
  id: number
  user_id: number
  estado_codigo: string
  total: number
  created_at: string
  cliente_email?: string | null
}

export interface PedidoDetalle {
  id: number
  cliente_id: number
  estado_codigo: string
  direccion_calle: string
  direccion_numero: string
  direccion_piso_depto?: string | null
  direccion_ciudad: string
  direccion_provincia: string
  direccion_codigo_postal?: string | null
  direccion_pais: string
  direccion_referencias?: string | null
  total: number
  costo_envio: number
  items: DetalleItem[]
  creado_en: string
  actualizado_en: string
}

export interface PaginatedPedidos {
  items: PedidoListItem[]
  total: number
  page: number
  size: number
  pages: number
}
