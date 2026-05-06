import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Producto {
  id: number
  nombre: string
  precio: number
  imagenUrl: string
}

export interface CartItem {
  productoId: number
  producto: Producto
  cantidad: number
  personalizacion: number[] // IDs de ingredientes a excluir
}

interface CartState {
  items: CartItem[]
  addItem: (producto: Producto, cantidad: number, personalizacion?: number[]) => void
  removeItem: (productoId: number) => void
  updateQuantity: (productoId: number, cantidad: number) => void
  clearCart: () => void
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (producto, cantidad, personalizacion = []) => {
        const items = get().items
        const existing = items.find((item) => item.productoId === producto.id)
        if (existing) {
          set({
            items: items.map((item) =>
              item.productoId === producto.id
                ? { ...item, cantidad: item.cantidad + cantidad }
                : item
            ),
          })
        } else {
          set({
            items: [
              ...items,
              {
                productoId: producto.id,
                producto,
                cantidad,
                personalizacion,
              },
            ],
          })
        }
      },
      removeItem: (productoId) => {
        set({ items: get().items.filter((item) => item.productoId !== productoId) })
      },
      updateQuantity: (productoId, cantidad) => {
        if (cantidad <= 0) {
          get().removeItem(productoId)
          return
        }
        set({
          items: get().items.map((item) =>
            item.productoId === productoId ? { ...item, cantidad } : item
          ),
        })
      },
      clearCart: () => set({ items: [] }),
    }),
    {
      name: 'food-store-cart',
      partialize: (state) => ({ items: state.items }),
    }
  )
)

// Selectores
export const selectItems = (state: CartState) => state.items
export const totalItems = () =>
  useCartStore.getState().items.reduce((sum, item) => sum + item.cantidad, 0)
export const totalPrice = () =>
  useCartStore.getState().items.reduce(
    (sum, item) => sum + item.producto.precio * item.cantidad,
    0
  )
export const getItem = (productoId: number) =>
  useCartStore.getState().items.find((item) => item.productoId === productoId)