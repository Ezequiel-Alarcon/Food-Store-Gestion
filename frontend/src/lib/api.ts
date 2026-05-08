import axios, { type AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Flag para evitar múltiples refresh simultáneos
let isRefreshing = false
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason?: unknown) => void
}> = []

const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else {
      promise.resolve(token)
    }
  })
  failedQueue = []
}

// Crear instancia de axios
export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Interceptor de request - agregar Authorization header
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = useAuthStore.getState().accessToken
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor de response - manejar 401 con refresh automático
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError<{ detail?: string }>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    // Si no es 401, o si ya fue reintentado, rechazar
    if (!error.response || error.response.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // Si es una solicitud de refresh, rechazar directamente
    if (originalRequest.url?.includes('/auth/refresh')) {
      return Promise.reject(error)
    }

    // Marcar como reintentado
    originalRequest._retry = true

    // Si ya hay un refresh en curso, esperar a que termine
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      })
        .then((token) => {
          if (token && originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${token}`
          }
          return api(originalRequest)
        })
        .catch((err) => Promise.reject(err))
    }

    // Iniciar refresh
    isRefreshing = true
    const refreshToken = useAuthStore.getState().refreshToken

    if (!refreshToken) {
      isRefreshing = false
      processQueue(error, null)
      useAuthStore.getState().logout()
      window.location.href = '/login'
      return Promise.reject(error)
    }

    try {
      // Intentar refresh del token
      const response = await api.post('/auth/refresh', {
        refreshToken,
      })

      const { accessToken: newAccessToken, refreshToken: newRefreshToken } = response.data

      // Actualizar tokens en el store
      useAuthStore.getState().updateTokens({
        accessToken: newAccessToken,
        refreshToken: newRefreshToken,
      })

      // Reintentar request original
      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
      }

      processQueue(null, newAccessToken)
      isRefreshing = false

      return api(originalRequest)
    } catch (refreshError) {
      processQueue(refreshError as AxiosError, null)
      isRefreshing = false

      // Refresh falló - logout y redirigir
      useAuthStore.getState().logout()
      window.location.href = '/login'
      return Promise.reject(refreshError)
    }
  }
)

// Tipos para la API
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  accessToken: string
  refreshToken: string
  user: {
    id: number
    nombre: string
    email: string
    roles: string[]
  }
}

export interface RegisterRequest {
  nombre: string
  email: string
  password: string
}

export interface RefreshRequest {
  refreshToken: string
}

export interface RefreshResponse {
  accessToken: string
  refreshToken: string
}

export interface ErrorResponse {
  detail: string
}