export interface UserAddress {
  id: number
  user_id: number
  etiqueta: string | null
  calle: string
  numero: string
  piso_depto: string | null
  ciudad: string
  provincia: string
  codigo_postal: string | null
  pais: string
  referencias: string | null
  is_default: boolean
  activa: boolean
}

export interface BranchAddress {
  id: number
  branch_id: number
  calle: string
  numero: string
  piso_depto: string | null
  ciudad: string
  provincia: string
  codigo_postal: string | null
  pais: string
  referencias: string | null
  activa: boolean
}

export type BranchAddressCreate = Omit<BranchAddress, 'id' | 'branch_id' | 'activa'>
export type BranchAddressUpdate = Partial<BranchAddressCreate>

export type UserAddressCreate = Omit<UserAddress, 'id' | 'user_id' | 'is_default' | 'activa'>
export type UserAddressUpdate = Partial<UserAddressCreate>

// --- Branch (Sucursal) types ---

export interface Branch {
  id: number
  nombre: string
  activa: boolean
  direccion?: BranchAddress | null
}

export type BranchCreate = { nombre: string }
export type BranchUpdate = { nombre?: string; activa?: boolean }
