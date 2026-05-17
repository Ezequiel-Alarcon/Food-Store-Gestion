export interface PerfilResponse {
  id: number
  email: string
  nombre: string
  apellido: string
  rol: string
  telefono: string | null
  activo: boolean
  created_at: string | null
}

export interface UpdateProfileRequest {
  nombre?: string | null
  apellido?: string | null
  telefono?: string | null
}

export interface ChangePasswordRequest {
  current_password: string
  new_password: string
}

export interface MessageResponse {
  message: string
}
