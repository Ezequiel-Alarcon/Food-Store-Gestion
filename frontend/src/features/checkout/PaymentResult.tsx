import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePagoStatus, useRetryPago } from '../../entities/pago/queries';
import { useUIStore } from '../../stores/uiStore';
import type { PaymentResultProps } from './types';

const STATUS_MESSAGES: Record<string, string> = {
    approved: 'approved',
    rejected: 'rejected',
    cc_rejected_insufficient_amount: 'Fondos insuficientes. Probá con otra tarjeta.',
    cc_rejected_card_disabled: 'Tarjeta rechazada. Contactá a tu banco o usá otra tarjeta.',
    cc_rejected_duplicated_payment: 'Ya existe un pago con este valor. Verificá tus pedidos.',
    cc_rejected_high_risk: 'El pago fue rechazado por seguridad. Intentá con otro medio de pago.',
    cc_rejected_max_attempts: 'Superaste el límite de intentos. Probá más tarde.',
    cc_rejected_other_reason: 'El pago fue rechazado. Intentá con otra tarjeta.',
    default: 'El pago fue rechazado. Intentá con otra tarjeta.',
};

function getRejectionMessage(statusDetail: string | null): string {
    if (!statusDetail) return STATUS_MESSAGES.default;
    return STATUS_MESSAGES[statusDetail] || STATUS_MESSAGES.default;
}

export function PaymentResult({ pagoResponse: initialPago, pedidoId, onRetry }: PaymentResultProps) {
    const navigate = useNavigate();
    const addToast = useUIStore((s) => s.addToast);
    const { data: pagoStatus, isError } = usePagoStatus(pedidoId, !initialPago);
    const { isPending: isRetrying } = useRetryPago();

    const pago = initialPago || pagoStatus;
    const status = pago?.status;

    const [pollCount, setPollCount] = useState(0);
    useEffect(() => {
        if (!initialPago && pagoStatus) {
            setPollCount((c) => c + 1);
        }
    }, [pagoStatus, initialPago]);

    const isTimedOut = pollCount >= 30;

    useEffect(() => {
        if (status === 'approved') {
            addToast('success', '¡Pago aprobado!');
        } else if (status === 'rejected') {
            addToast('error', getRejectionMessage(pago?.status_detail ?? null));
        }
    }, [status, pago?.status_detail, addToast]);

    if (!pago && !isError && !isTimedOut) {
        return (
            <div className="flex flex-col items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4" />
                <p className="text-gray-600 text-lg">Procesando tu pago...</p>
                <p className="text-gray-400 text-sm mt-1">Esto puede tomar unos segundos</p>
            </div>
        );
    }

    if (isTimedOut || (isError && !pago)) {
        return (
            <div className="text-center py-8">
                <div className="text-yellow-500 text-5xl mb-4">⏳</div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">Verificación pendiente</h2>
                <p className="text-gray-500 mb-6">
                    Tu pago está siendo procesado. Podés ver el estado en la sección de pedidos.
                </p>
                <button
                    onClick={() => navigate(`/pedidos/${pedidoId}`)}
                    className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                >
                    Ver estado del pedido
                </button>
            </div>
        );
    }

    if (status === 'approved') {
        const amount = pago?.transaction_amount ?? 0;
        const method = pago?.payment_method_id ?? '';
        const formatMethod = (m: string) => {
            const methods: Record<string, string> = { visa: 'Visa', master: 'Mastercard', amex: 'American Express', debvisa: 'Visa Débito', debmaster: 'Mastercard Débito' };
            return methods[m] || m;
        };

        return (
            <div className="text-center py-8">
                <div className="text-green-500 text-5xl mb-4">✓</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">¡Pago aprobado!</h2>
                <div className="bg-white rounded-lg shadow-sm p-4 mt-4 text-left space-y-2">
                    <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Método</span>
                        <span className="font-medium">{formatMethod(method)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Monto</span>
                        <span className="font-medium">${amount.toLocaleString('es-AR')}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Pedido</span>
                        <span className="font-medium">#{pedidoId}</span>
                    </div>
                </div>
                <div className="flex gap-3 mt-6">
                    <button
                        onClick={() => navigate(`/pedidos/${pedidoId}`)}
                        className="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                    >
                        Ver pedido
                    </button>
                    <button
                        onClick={() => navigate('/productos')}
                        className="flex-1 bg-white text-indigo-600 border border-indigo-600 py-2 rounded-lg hover:bg-indigo-50 transition-colors"
                    >
                        Seguir comprando
                    </button>
                </div>
            </div>
        );
    }

    if (status === 'rejected') {
        return (
            <div className="text-center py-8">
                <div className="text-red-500 text-5xl mb-4">✕</div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">Pago rechazado</h2>
                <p className="text-gray-500 mb-6">{getRejectionMessage(pago?.status_detail ?? null)}</p>
                <div className="flex gap-3">
                    <button
                        onClick={onRetry}
                        disabled={isRetrying}
                        className="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                    >
                        {isRetrying ? 'Reintentando...' : 'Reintentar con otra tarjeta'}
                    </button>
                    <button
                        onClick={() => navigate(`/pedidos/${pedidoId}`)}
                        className="flex-1 bg-white text-gray-700 border border-gray-300 py-2 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                        Cancelar
                    </button>
                </div>
            </div>
        );
    }

    // Still processing (in_process, pending)
    return (
        <div className="flex flex-col items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4" />
            <p className="text-gray-600 text-lg">Procesando tu pago...</p>
        </div>
    );
}
