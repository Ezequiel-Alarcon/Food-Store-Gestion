/** Tipos para el módulo de administración de usuarios */

export interface UserAdmin {
  id: number
  email: string
  nombre: string
  apellido: string
  rol: 'ADMIN' | 'STOCK' | 'PEDIDOS' | 'CLIENT'
  telefono: string | null
  activo: boolean
  created_at: string | null
}

export interface UserUpdatePayload {
  nombre?: string
  apellido?: string
  rol?: string
  telefono?: string
  activo?: boolean
}

export const ROLES = ['ADMIN', 'STOCK', 'PEDIDOS', 'CLIENT'] as const
export type RolValue = (typeof ROLES)[number]