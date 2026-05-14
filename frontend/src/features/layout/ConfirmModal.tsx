import { useUIStore } from '../../stores/uiStore'

export function ConfirmModal() {
  const confirmModal = useUIStore((s) => s.confirmModal)
  const closeConfirmModal = useUIStore((s) => s.closeConfirmModal)

  if (!confirmModal.open) return null

  const handleConfirm = () => {
    try { confirmModal.onConfirm?.() } finally { closeConfirmModal() }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/50" onClick={closeConfirmModal} />

      {/* Modal */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-sm w-full mx-4 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {confirmModal.title}
        </h3>
        <p className="text-sm text-gray-600 mb-6">{confirmModal.message}</p>

        <div className="flex justify-end gap-3">
          <button
            onClick={closeConfirmModal}
            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 border border-gray-300 rounded-lg"
          >
            Cancelar
          </button>
          <button
            onClick={handleConfirm}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>
  )
}
