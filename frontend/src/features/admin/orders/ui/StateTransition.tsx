import { useState } from 'react'
import { api } from '../../../../lib/api'
import { useUIStore } from '../../../../stores/uiStore'

interface StateTransitionProps {
  pedidoId: number
  estadoActual: string
  onTransitionComplete: () => void
}

const TRANSICIONES_VALIDAS: Record<string, string[]> = {
  PENDIENTE: ['CANCELADO'],
  CONFIRMADO: ['EN_PREP', 'CANCELADO'],
  EN_PREP: ['EN_CAMINO', 'CANCELADO'],
  EN_CAMINO: ['ENTREGADO'],
  ENTREGADO: [],
  CANCELADO: [],
}

const ESTADOS_TERMINALES = new Set(['ENTREGADO', 'CANCELADO'])

const LABELS: Record<string, string> = {
  EN_PREP: 'Avanzar a En Preparación',
  EN_CAMINO: 'Avanzar a En Camino',
  ENTREGADO: 'Marcar como Entregado',
  CANCELADO: 'Cancelar pedido',
}

export function StateTransition({
  pedidoId,
  estadoActual,
  onTransitionComplete,
}: StateTransitionProps) {
  const addToast = useUIStore((s) => s.addToast)
  const [loadingTarget, setLoadingTarget] = useState<string | null>(null)
  const [motivo, setMotivo] = useState('')
  const [cancelling, setCancelling] = useState(false)

  const transiciones = TRANSICIONES_VALIDAS[estadoActual] || []

  if (ESTADOS_TERMINALES.has(estadoActual) || transiciones.length === 0) {
    return null
  }

  async function handleTransition(target: string) {
    setLoadingTarget(target)
    try {
      const body: Record<string, string> = { nuevo_estado: target }
      if (target === 'CANCELADO') {
        body.motivo = motivo
      }
      await api.patch(`/pedidos/${pedidoId}/estado`, body)
      addToast('success', `Pedido #${pedidoId} actualizado a ${target}`)
      setMotivo('')
      setCancelling(false)
      onTransitionComplete()
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      addToast('error', detail || 'Error al actualizar el estado del pedido')
    } finally {
      setLoadingTarget(null)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Transiciones de Estado</h3>

      <div className="flex flex-wrap gap-3">
        {transiciones.map((target) => {
          if (target === 'CANCELADO') {
            if (!cancelling) {
              return (
                <button
                  key={target}
                  type="button"
                  onClick={() => setCancelling(true)}
                  className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm font-medium transition-colors"
                >
                  {LABELS[target] || target}
                </button>
              )
            }
            return (
              <div key={target} className="w-full space-y-3">
                <textarea
                  className="w-full border border-gray-300 rounded p-2 text-sm"
                  rows={3}
                  placeholder="Motivo de cancelación (obligatorio)"
                  value={motivo}
                  onChange={(e) => setMotivo(e.target.value)}
                />
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => handleTransition(target)}
                    disabled={loadingTarget === target || !motivo.trim()}
                    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loadingTarget === target ? 'Procesando...' : 'Confirmar cancelación'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setCancelling(false)
                      setMotivo('')
                    }}
                    className="px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    Volver
                  </button>
                </div>
              </div>
            )
          }

          return (
            <button
              key={target}
              type="button"
              onClick={() => handleTransition(target)}
              disabled={loadingTarget === target}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loadingTarget === target ? 'Procesando...' : (LABELS[target] || `Avanzar a ${target}`)}
            </button>
          )
        })}
      </div>
    </div>
  )
}
