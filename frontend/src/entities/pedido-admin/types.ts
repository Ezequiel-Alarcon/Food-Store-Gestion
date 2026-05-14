/** Tipos para el módulo de pedidos (vista admin/gestor) */

export interface OrderAdminItem {
  /** ID único del pedido */
  id: number
  /** ID del usuario cliente */
  user_id: number
  /** Código de estado (PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO) */
  estado_codigo: string
  /** Total del pedido (incluye envío) */
  total: number
  /** Fecha de creación del pedido */
  created_at: string
  /** Email del cliente (solo visible para ADMIN/PEDIDOS) */
  cliente_email: string | null
}

export interface OrderAdminDetail {
  id: number
  cliente_id: number
  estado_codigo: string
  /** Datos del cliente */
  cliente_email?: string | null
  cliente_nombre?: string | null
  cliente_apellido?: string | null
  /** Dirección de entrega */
  direccion_calle: string
  direccion_numero: string
  direccion_piso_depto: string | null
  direccion_ciudad: string
  direccion_provincia: string
  direccion_codigo_postal: string | null
  direccion_pais: string
  direccion_referencias: string | null
  /** Montos */
  total: number
  costo_envio: number
  /** Items del pedido */
  items: OrderItemDetail[]
  /** Fechas */
  creado_en: string
  actualizado_en: string
}

export interface OrderItemDetail {
  id: number
  producto_id: number
  cantidad: number
  precio_unitario: number
  exclusiones: number[]
  /** Nombre del producto (viene del backend en el detalle) */
  producto_nombre?: string
}

export interface OrderHistoryItem {
  id: number
  estado_anterior_codigo: string | null
  estado_nuevo_codigo: string
  actor_id: number | null
  actor_tipo: string
  motivo: string | null
  creado_en: string
}

/** Filtros para listar pedidos admin */
export interface OrderAdminFilters {
  page?: number
  size?: number
  /** Filtrar por estado */
  estado?: string
  /** Búsqueda por email del cliente */
  q?: string
  /** Fecha desde */
  desde?: string
  /** Fecha hasta */
  hasta?: string
}

/** Respuesta paginada */
export interface PaginatedOrdersAdmin {
  items: OrderAdminItem[]
  total: number
  page: number
  size: number
  pages: number
}