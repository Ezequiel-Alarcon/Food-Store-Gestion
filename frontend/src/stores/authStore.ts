import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api, type LoginRequest, type LoginResponse, type RegisterRequest, type PerfilResponse } from '../lib/api'

export interface User {
  id: number
  nombre: string
  email: string
  roles: string[]
}

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (credentials: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  updateTokens: (tokens: { accessToken: string; refreshToken: string }) => void
  setUser: (user: User) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: LoginRequest) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.post<LoginResponse>('/auth/login', credentials)
          const { access_token, refresh_token } = response.data
          set({ accessToken: access_token, refreshToken: refresh_token })
          try {
            const perfilRes = await api.get<PerfilResponse>('/perfil')
            const p = perfilRes.data
            set({ user: { id: p.id, nombre: p.nombre, email: p.email, roles: [p.rol] }, isAuthenticated: true, isLoading: false, error: null })
          } catch {
            set({ isAuthenticated: true, isLoading: false, error: null })
          }
        } catch (error: unknown) {
          const err = error as { response?: { data?: { detail?: string } } }
          set({ isLoading: false, error: err.response?.data?.detail || 'Error al iniciar sesión' })
          throw error
        }
      },

      register: async (data: RegisterRequest) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.post<LoginResponse>('/auth/register', data)
          const { access_token, refresh_token } = response.data
          set({ accessToken: access_token, refreshToken: refresh_token })
          try {
            const perfilRes = await api.get<PerfilResponse>('/perfil')
            const p = perfilRes.data
            set({ user: { id: p.id, nombre: p.nombre, email: p.email, roles: [p.rol] }, isAuthenticated: true, isLoading: false, error: null })
          } catch {
            set({ isAuthenticated: true, isLoading: false, error: null })
          }
        } catch (error: unknown) {
          const err = error as { response?: { data?: { detail?: string | Array<{ msg: string }> } } }
          const detail = err.response?.data?.detail
          const message = Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : (detail || 'Error al registrarse')
          set({ isLoading: false, error: message })
          throw error
        }
      },

      logout: () => {
        set({
          accessToken: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
        window.location.href = '/'
      },

      updateTokens: (tokens) => set(tokens),

      setUser: (user) => set({ user }),

      clearError: () => set({ error: null }),
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Selectores
export const selectIsAuthenticated = (state: AuthState) => state.isAuthenticated
export const selectUser = (state: AuthState) => state.user
export const selectAccessToken = (state: AuthState) => state.accessToken

// Helper functions
export const isAuthenticated = () => useAuthStore.getState().isAuthenticated
export const hasRole = (role: string) => {
  const user = useAuthStore.getState().user
  return user?.roles.includes(role) ?? false
}