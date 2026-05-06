import { create } from 'zustand'
import { persist } from 'zustand/middleware'

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
  login: (tokens: { accessToken: string; refreshToken: string }, user: User) => void
  logout: () => void
  updateTokens: (tokens: { accessToken: string; refreshToken: string }) => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      login: (tokens, user) =>
        set({
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
          user,
          isAuthenticated: true,
        }),
      logout: () =>
        set({
          accessToken: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
        }),
      updateTokens: (tokens) =>
        set({
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
        }),
      setUser: (user) => set({ user }),
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({ accessToken: state.accessToken }),
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