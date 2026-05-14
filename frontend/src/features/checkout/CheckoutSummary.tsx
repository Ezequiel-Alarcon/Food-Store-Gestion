import { useCartStore, totalPrice } from '../../stores/cartStore';
import { useUserAddresses } from '../../entities/addresses/queries';
import type { UserAddress } from '../../entities/addresses/types';
import type { CheckoutSummaryProps } from './types';

export function CheckoutSummary({ pedidoId: _pedidoId, selectedAddressId, onConfirm }: CheckoutSummaryProps) {
    const items = useCartStore((s) => s.items);
    const { data: addresses } = useUserAddresses();
    const address = addresses?.find((a: UserAddress) => a.id === selectedAddressId);

    if (items.length === 0) {
        return (
            <div className="text-center py-8">
                <p className="text-gray-500">Tu carrito está vacío</p>
            </div>
        );
    }

    const total = totalPrice();

    return (
        <div className="space-y-6">
            {/* Order Items */}
            <div className="bg-white rounded-lg shadow-sm p-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Resumen del pedido</h3>
                <div className="divide-y divide-gray-100">
                    {items.map((item) => (
                        <div key={item.productoId} className="flex justify-between py-3">
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900 truncate">{item.producto.nombre}</p>
                                <p className="text-xs text-gray-500">Cantidad: {item.cantidad}</p>
                            </div>
                            <p className="text-sm font-medium text-gray-900 ml-4">
                                ${(item.producto.precio * item.cantidad).toLocaleString('es-AR')}
                            </p>
                        </div>
                    ))}
                </div>
                <div className="border-t border-gray-200 mt-4 pt-4 flex justify-between">
                    <span className="text-base font-semibold text-gray-900">Total</span>
                    <span className="text-base font-semibold text-gray-900">
                        ${total.toLocaleString('es-AR')}
                    </span>
                </div>
            </div>

            {/* Delivery Address */}
            {address && (
                <div className="bg-white rounded-lg shadow-sm p-4">
                    <h3 className="text-sm font-semibold text-gray-900 mb-1">Dirección de entrega</h3>
                    <p className="text-sm text-gray-600">
                        {address.calle} {address.numero}
                    </p>
                    <p className="text-sm text-gray-500">
                        {[address.ciudad, address.provincia].filter(Boolean).join(', ')}
                    </p>
                </div>
            )}

            {/* Confirm Button */}
            <button
                onClick={onConfirm}
                className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
            >
                Confirmar y pagar
            </button>
        </div>
    );
}
