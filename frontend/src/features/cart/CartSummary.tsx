import { Link } from 'react-router-dom'
import { useCartStore, totalPrice } from '../../stores/cartStore'
import { useUIStore } from '../../stores/uiStore'

export function CartSummary() {
  const items = useCartStore((s) => s.items)
  const removeItem = useCartStore((s) => s.removeItem)
  const updateQuantity = useCartStore((s) => s.updateQuantity)
  const clearCart = useCartStore((s) => s.clearCart)
  const addToast = useUIStore((s) => s.addToast)
  const openConfirmModal = useUIStore((s) => s.openConfirmModal)
  const closeCart = useUIStore((s) => s.closeCart)

  const total = totalPrice()

  const handleClearCart = () => {
    openConfirmModal('Vaciar carrito', '¿Eliminar todos los productos?', () => {
      clearCart()
      addToast('info', 'Carrito vaciado')
    })
  }

  // ── Empty state ──
  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
        <div className="w-14 h-14 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <svg className="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
          </svg>
        </div>
        <p className="text-sm font-medium text-gray-500">Carrito vacío</p>
        <p className="text-xs text-gray-400 mt-1">Agregá productos del catálogo</p>
        <Link
          to="/productos"
          onClick={closeCart}
          className="mt-5 px-5 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
        >
          Ver productos
        </Link>
      </div>
    )
  }

  // ── Items + Footer ──
  return (
    <div className="flex flex-col flex-1">
      {/* Item list */}
      <div className="flex-1 overflow-y-auto">
        {items.map((item) => (
          <div key={item.productoId} className="px-4 py-3 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
            <div className="flex gap-2.5">
              {/* Thumbnail */}
              <div className="w-10 h-10 rounded-md bg-gray-100 overflow-hidden flex-shrink-0">
                <img
                  src={item.producto.imagenUrl || 'https://placehold.co/80x80/e2e8f0/64748b?text=+'}
                  alt={item.producto.nombre}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start">
                  <h4 className="text-xs font-medium text-gray-900 leading-tight pr-1 line-clamp-2">
                    {item.producto.nombre}
                  </h4>
                  <button
                    onClick={() => {
                      removeItem(item.productoId)
                      addToast('info', 'Eliminado')
                    }}
                    className="text-gray-300 hover:text-red-400 flex-shrink-0 ml-1"
                  >
                    <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* Exclusiones */}
                {item.personalizacion.length > 0 && (
                  <p className="text-[10px] text-orange-500 mt-0.5">
                    −{item.personalizacion.length} ingrediente(s)
                  </p>
                )}

                {/* Cantidad + Precio */}
                <div className="flex items-center justify-between mt-1.5">
                  <div className="flex items-center border border-gray-200 rounded-md">
                    <button
                      onClick={() => updateQuantity(item.productoId, item.cantidad - 1)}
                      className="w-6 h-6 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 text-xs rounded-l-md transition-colors"
                    >
                      −
                    </button>
                    <span className="w-7 h-6 flex items-center justify-center text-xs font-medium text-gray-700 border-x border-gray-200">
                      {item.cantidad}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.productoId, item.cantidad + 1)}
                      className="w-6 h-6 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 text-xs rounded-r-md transition-colors"
                    >
                      +
                    </button>
                  </div>
                  <span className="text-xs font-semibold text-gray-900">
                    ${(item.producto.precio * item.cantidad).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer — sticky */}
      <div className="border-t border-gray-100 px-4 py-3 space-y-2 bg-white">
        <div className="flex justify-between items-center">
          <span className="text-xs font-medium text-gray-500">
            {items.reduce((s, i) => s + i.cantidad, 0)} producto(s)
          </span>
          <span className="text-base font-bold text-indigo-600">
            ${total.toFixed(2)}
          </span>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleClearCart}
            className="flex-1 py-1.5 text-xs font-medium text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
          >
            Vaciar
          </button>
        </div>
      </div>
    </div>
  )
}
