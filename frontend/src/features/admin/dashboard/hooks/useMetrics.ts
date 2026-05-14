/**
 * Hook compuesto que combina las 4 queries de métricas y expone
 * el estado unificado con soporte para filtrado por rango de fechas.
 */
import { useState } from 'react'
import {
  useGeneralMetrics,
  useSalesChart,
  useTopProducts,
  useOrdersByStatus,
} from '../api'
import type { DateRange } from '../types'

interface MetricsHookResult {
  // Datos
  metrics: ReturnType<typeof useGeneralMetrics>['data']
  salesChart: ReturnType<typeof useSalesChart>['data']
  topProducts: ReturnType<typeof useTopProducts>['data']
  ordersByStatus: ReturnType<typeof useOrdersByStatus>['data']
  // Estado de carga
  isLoading: boolean
  isError: boolean
  error: Error | null
  // Refetch
  refetch: () => void
  // Filtro de fechas
  dateRange: DateRange
  setDateRange: (range: DateRange) => void
}

/**
 * Hook unificado para acceder a todas las métricas del dashboard.
 * Combina las 4 queries y expone estado de carga centralizado.
 *
 * @example
 * ```tsx
 * const { metrics, salesChart, isLoading, dateRange, setDateRange } = useMetrics()
 * ```
 */
export function useMetrics(): MetricsHookResult {
  const [dateRange, setDateRange] = useState<DateRange>(30)

  // Queries individuales
  const generalMetrics = useGeneralMetrics()
  const salesChart = useSalesChart()
  const topProducts = useTopProducts()
  const ordersByStatus = useOrdersByStatus()

  // Estado unificado de carga
  const isLoading =
    generalMetrics.isLoading ||
    salesChart.isLoading ||
    topProducts.isLoading ||
    ordersByStatus.isLoading

  // Estado unificado de error
  const isError =
    generalMetrics.isError ||
    salesChart.isError ||
    topProducts.isError ||
    ordersByStatus.isError

  const error =
    generalMetrics.error ||
    salesChart.error ||
    topProducts.error ||
    ordersByStatus.error ||
    null

  // Función para re-fetch de todas las queries
  const refetch = () => {
    generalMetrics.refetch()
    salesChart.refetch()
    topProducts.refetch()
    ordersByStatus.refetch()
  }

  return {
    // Datos
    metrics: generalMetrics.data,
    salesChart: salesChart.data,
    topProducts: topProducts.data,
    ordersByStatus: ordersByStatus.data,
    // Estado
    isLoading,
    isError,
    error,
    refetch,
    // Filtro
    dateRange,
    setDateRange,
  }
}