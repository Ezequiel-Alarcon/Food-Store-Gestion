/**
 * Tipos para el dashboard de métricas administrativas.
 * Mapean los schemas del backend en backend/app/modules/admin/schemas.py
 */

export interface GeneralMetrics {
  total_pedidos: number
  total_revenue: number
  ticket_promedio: number
  total_clientes: number
}

export interface SalesChartEntry {
  fecha: string // ISO date string
  total_pedidos: number
  revenue: number
}

export interface SalesChartResponse {
  datos: SalesChartEntry[]
  dias: number
}

export interface TopProductEntry {
  producto_id: number
  nombre: string
  cantidad_vendida: number
}

export interface OrdersByStatusEntry {
  estado_codigo: string
  cantidad: number
}

export type DateRange = 7 | 30 | 90