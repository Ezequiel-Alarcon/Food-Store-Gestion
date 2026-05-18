import { Link, useNavigate } from 'react-router-dom'
import { useCartStore, totalPrice } from '../stores/cartStore'
import { useUIStore } from '../stores/uiStore'
import { useUserAddresses } from '../entities/addresses/queries'
import { useCreatePedido } from '../entities/pedido'

/**
 * Página dedicada del carrito. Reutiliza la misma lógica que CartSummary
 * pero en un layout de página completa (no drawer).
 */
export function CartPage() {
  const items = useCartStore((s) => s.items)
  const removeItem = useCartStore((s) => s.removeItem)
  const updateQuantity = useCartStore((s) => s.updateQuantity)
  const clearCart = useCartStore((s) => s.clearCart)
  const addToast = useUIStore((s) => s.addToast)
  const openConfirmModal = useUIStore((s) => s.openConfirmModal)

  const total = totalPrice()

  const navigate = useNavigate()
  const { mutateAsync: createPedido, isPending: isCreating } = useCreatePedido()
  const { data: addresses } = useUserAddresses()

  const handleCheckout = async () => {
    if (!addresses || addresses.length === 0) {
      addToast('error', 'Necesitás una dirección de entrega. Agregala en "Mis Direcciones".')
      return
    }

    if (isCreating || items.length === 0) return

    try {
      const pedido = await createPedido({
        direccion_id: addresses[0].id,
        items: items.map((item) => ({
          producto_id: item.productoId,
          cantidad: item.cantidad,
          exclusiones: item.personalizacion,
        })),
      })

      clearCart() // Limpiar carrito después de crear el pedido para evitar duplicados
      addToast('success', '¡Pedido creado! Completá el pago para confirmarlo.')
      navigate(`/checkout?pedido=${pedido.id}`)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al crear el pedido'
      addToast('error', message)
    }
  }

  const handleClearCart = () => {
    openConfirmModal(
      'Vaciar carrito',
      '¿Estás seguro de que querés eliminar todos los productos del carrito?',
      () => {
        clearCart()
        addToast('info', 'Carrito vaciado')
      }
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Tu Carrito</h1>

      {items.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Tu carrito está vacío</p>
          <Link
            to="/productos"
            className="inline-block mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Ver Productos
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow">
          <div className="divide-y divide-gray-100">
            {items.map((item) => (
              <div key={item.productoId} className="p-4 sm:p-6">
                <div className="flex gap-4">
                  <div className="w-20 h-20 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                    <img
                      src={
                        item.producto.imagenUrl ||
                        'https://placehold.co/200x200/e2e8f0/64748b?text=Sin+Imagen'
                      }
                      alt={item.producto.nombre}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-base font-medium text-gray-900 truncate">
                      {item.producto.nombre}
                    </h3>
                    <p className="text-indigo-600 font-semibold mt-1">
                      ${item.producto.precio.toFixed(2)} c/u
                    </p>
                    {item.personalizacion.length > 0 && (
                      <p className="text-xs text-orange-600 mt-1">
                        Sin: {item.personalizacion.length} ingrediente(s)
                      </p>
                    )}
                    <div className="flex items-center justify-between mt-3">
                      <div className="flex items-center border border-gray-200 rounded">
                        <button
                          onClick={() => updateQuantity(item.productoId, item.cantidad - 1)}
                          className="px-3 py-1 text-gray-500 hover:text-gray-700 hover:bg-gray-50"
                        >
                          −
                        </button>
                        <span className="px-4 py-1 text-sm text-gray-900 border-x border-gray-200">
                          {item.cantidad}
                        </span>
                        <button
                          onClick={() => updateQuantity(item.productoId, item.cantidad + 1)}
                          className="px-3 py-1 text-gray-500 hover:text-gray-700 hover:bg-gray-50"
                        >
                          +
                        </button>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-base font-semibold text-gray-900">
                          ${(item.producto.precio * item.cantidad).toFixed(2)}
                        </span>
                        <button
                          onClick={() => {
                            removeItem(item.productoId)
                            addToast('info', `${item.producto.nombre} eliminado`)
                          }}
                          className="text-gray-300 hover:text-red-500 p-1"
                        >
                          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="border-t border-gray-200 p-6">
            <div className="flex justify-between items-center mb-4">
              <span className="text-lg font-semibold text-gray-900">Total</span>
              <span className="text-2xl font-bold text-indigo-600">
                ${total.toFixed(2)}
              </span>
            </div>
            <button
              onClick={handleCheckout}
              disabled={isCreating || items.length === 0}
              className="w-full py-3 px-4 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors mb-3"
            >
              {isCreating ? 'Creando pedido...' : 'Finalizar pedido'}
            </button>
            <div className="flex gap-3">
              <button
                onClick={handleClearCart}
                className="flex-1 py-2 text-sm font-medium text-red-600 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
              >
                Vaciar carrito
              </button>
              <Link
                to="/productos"
                className="flex-1 py-2 text-sm font-medium text-white bg-indigo-600 text-center rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Seguir comprando
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
