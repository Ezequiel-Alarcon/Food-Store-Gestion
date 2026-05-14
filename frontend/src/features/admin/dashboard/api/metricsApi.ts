/**
 * Queries TanStack Query para métricas administrativas.
 * Endpoints: /api/v1/admin/metrics/*
 */
import { useQuery } from '@tanstack/react-query'
import { api } from '../../../../lib/api'
import type {
  GeneralMetrics,
  SalesChartResponse,
  TopProductEntry,
  OrdersByStatusEntry,
} from '../types'

// Fetch functions
async function fetchGeneralMetrics(): Promise<GeneralMetrics> {
  const response = await api.get<GeneralMetrics>('/admin/metrics/')
  return response.data
}

async function fetchSalesChart(): Promise<SalesChartResponse> {
  const response = await api.get<SalesChartResponse>('/admin/metrics/sales-chart/')
  return response.data
}

async function fetchTopProducts(): Promise<TopProductEntry[]> {
  const response = await api.get<TopProductEntry[]>('/admin/metrics/top-products/')
  return response.data
}

async function fetchOrdersByStatus(): Promise<OrdersByStatusEntry[]> {
  const response = await api.get<OrdersByStatusEntry[]>('/admin/metrics/orders-by-status/')
  return response.data
}

// TanStack Query hooks
export function useGeneralMetrics() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'general'],
    queryFn: fetchGeneralMetrics,
    staleTime: 30 * 1000, // 30 segundos
  })
}

export function useSalesChart() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'sales-chart'],
    queryFn: fetchSalesChart,
    staleTime: 30 * 1000,
  })
}

export function useTopProducts() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'top-products'],
    queryFn: fetchTopProducts,
    staleTime: 60 * 1000, // 1 minuto
  })
}

export function useOrdersByStatus() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'orders-by-status'],
    queryFn: fetchOrdersByStatus,
    staleTime: 30 * 1000,
  })
}