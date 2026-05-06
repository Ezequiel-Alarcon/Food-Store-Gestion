import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
  id: string
  type: ToastType
  message: string
}

interface ConfirmModal {
  open: boolean
  title: string
  message: string
  onConfirm: (() => void) | null
}

interface UIState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  cartOpen: boolean
  confirmModal: ConfirmModal
  toasts: Toast[]
  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
  openCart: () => void
  closeCart: () => void
  toggleCart: () => void
  openConfirmModal: (title: string, message: string, onConfirm: () => void) => void
  closeConfirmModal: () => void
  addToast: (type: ToastType, message: string) => void
  removeToast: (id: string) => void
}

const generateToastId = () => `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      theme: 'light',
      sidebarOpen: false,
      cartOpen: false,
      confirmModal: {
        open: false,
        title: '',
        message: '',
        onConfirm: null,
      },
      toasts: [],
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set({ sidebarOpen: !get().sidebarOpen }),
      openCart: () => set({ cartOpen: true }),
      closeCart: () => set({ cartOpen: false }),
      toggleCart: () => set({ cartOpen: !get().cartOpen }),
      openConfirmModal: (title, message, onConfirm) =>
        set({
          confirmModal: { open: true, title, message, onConfirm },
        }),
      closeConfirmModal: () =>
        set({
          confirmModal: { open: false, title: '', message: '', onConfirm: null },
        }),
      addToast: (type, message) => {
        const id = generateToastId()
        const toast: Toast = { id, type, message }
        set({ toasts: [...get().toasts, toast] })
        // Auto-remove after 5 seconds
        setTimeout(() => get().removeToast(id), 5000)
      },
      removeToast: (id) => {
        set({ toasts: get().toasts.filter((t) => t.id !== id) })
      },
    }),
    {
      name: 'food-store-ui',
      partialize: (state) => ({ theme: state.theme }),
    }
  )
)