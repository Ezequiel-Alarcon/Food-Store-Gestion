/** Constantes y utilidades para el módulo de pedidos admin */

export const ESTADOS = [
  'PENDIENTE',
  'CONFIRMADO',
  'EN_PREP',
  'EN_CAMINO',
  'ENTREGADO',
  'CANCELADO',
] as const

export const ESTADO_COLORS: Record<string, string> = {
  PENDIENTE: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  CONFIRMADO: 'bg-blue-100 text-blue-800 border-blue-200',
  EN_PREP: 'bg-purple-100 text-purple-800 border-purple-200',
  EN_CAMINO: 'bg-indigo-100 text-indigo-800 border-indigo-200',
  ENTREGADO: 'bg-green-100 text-green-800 border-green-200',
  CANCELADO: 'bg-red-100 text-red-800 border-red-200',
}

export const ESTADO_LABELS: Record<string, string> = {
  PENDIENTE: 'Pendiente',
  CONFIRMADO: 'Confirmado',
  EN_PREP: 'En preparación',
  EN_CAMINO: 'En camino',
  ENTREGADO: 'Entregado',
  CANCELADO: 'Cancelado',
}

/** Formatear fecha a formato argentino DD/MM/YYYY HH:mm */
export function formatDateArgentina(dateString: string): string {
  const date = new Date(dateString)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} ${hours}:${minutes}`
}

/** Formatear monto en pesos argentinos */
export function formatCurrencyARS(amount: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 2,
  }).format(amount)
}