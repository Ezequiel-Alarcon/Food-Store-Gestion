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

const STATUS_UI: Record<string, { icon: string; bg: string; title: string; message: string }> = {
    approved: { icon: '✅', bg: 'bg-green-50 border-green-200', title: '¡Pago aprobado!', message: 'Tu pedido será preparado pronto.' },
    pending: { icon: '⏳', bg: 'bg-yellow-50 border-yellow-200', title: 'Pago pendiente', message: 'Estamos esperando la confirmación del pago.' },
    in_process: { icon: '🔄', bg: 'bg-blue-50 border-blue-200', title: 'Pago en revisión', message: 'MercadoPago está revisando tu pago.' },
    rejected: { icon: '❌', bg: 'bg-red-50 border-red-200', title: 'Pago rechazado', message: '' },
    cancelled: { icon: '⊘', bg: 'bg-gray-50 border-gray-200', title: 'Pago cancelado', message: 'Podés intentar nuevamente.' },
};

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

    // Initial loading — no pago data yet
    if (!pago && !isError && !isTimedOut) {
        return (
            <div className="flex flex-col items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4" />
                <p className="text-gray-600 text-lg">Procesando tu pago...</p>
                <p className="text-gray-400 text-sm mt-1">Esto puede tomar unos segundos</p>
            </div>
        );
    }

    // Timed out or error with no pago data
    if (isTimedOut || (isError && !pago)) {
        return (
            <div className="text-center py-8">
                <div className="text-yellow-500 text-5xl mb-4">⏳</div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">Verificación pendiente</h2>
                <p className="text-gray-500 mb-6">
                    Tu pago está siendo procesado. Podés ver el estado en la sección de pedidos.
                </p>
                <button
                    onClick={() => navigate('/pedidos')}
                    className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                >
                    Ver estado del pedido
                </button>
            </div>
        );
    }

    // Known statuses — render specific card
    if (status && STATUS_UI[status]) {
        const ui = STATUS_UI[status];
        const displayMessage = status === 'rejected' ? getRejectionMessage(pago?.status_detail ?? null) : ui.message;
        const amount = pago?.transaction_amount ?? 0;
        const method = pago?.payment_method_id ?? '';

        const formatMethod = (m: string) => {
            const methods: Record<string, string> = { visa: 'Visa', master: 'Mastercard', amex: 'American Express', debvisa: 'Visa Débito', debmaster: 'Mastercard Débito' };
            return methods[m] || m;
        };

        return (
            <div className="py-4">
                <div className={`rounded-lg border p-6 ${ui.bg}`}>
                    <div className="text-center">
                        <span className="text-4xl">{ui.icon}</span>
                        <h2 className="text-xl font-bold text-gray-900 mt-3">{ui.title}</h2>
                        {displayMessage && <p className="text-gray-600 mt-1">{displayMessage}</p>}
                    </div>

                    {/* Payment details for approved */}
                    {status === 'approved' && (
                        <div className="mt-4 bg-white rounded-lg p-4 text-left space-y-2">
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
                    )}

                    {/* Actions per status */}
                    {status === 'approved' && (
                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => navigate('/pedidos')}
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
                    )}

                    {status === 'rejected' && (
                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={onRetry}
                                disabled={isRetrying}
                                className="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                            >
                                {isRetrying ? 'Reintentando...' : 'Reintentar con otra tarjeta'}
                            </button>
                            <button
                                onClick={() => navigate('/pedidos')}
                                className="flex-1 bg-white text-gray-700 border border-gray-300 py-2 rounded-lg hover:bg-gray-50 transition-colors"
                            >
                                Cancelar
                            </button>
                        </div>
                    )}

                    {status === 'cancelled' && (
                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={onRetry}
                                disabled={isRetrying}
                                className="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                            >
                                {isRetrying ? 'Reintentando...' : 'Reintentar pago'}
                            </button>
                            <button
                                onClick={() => navigate('/pedidos')}
                                className="flex-1 bg-white text-gray-700 border border-gray-300 py-2 rounded-lg hover:bg-gray-50 transition-colors"
                            >
                                Cancelar
                            </button>
                        </div>
                    )}

                    {/* Polling indicator for pending / in_process */}
                    {(status === 'pending' || status === 'in_process') && (
                        <div className="mt-4 text-center text-sm text-gray-500">
                            <div className="animate-spin inline-block h-4 w-4 border-b-2 border-indigo-600 mr-2 align-middle" />
                            <span className="align-middle">Consultando estado...</span>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    // Unknown status fallback
    return (
        <div className="flex flex-col items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4" />
            <p className="text-gray-600 text-lg">Procesando tu pago...</p>
            <p className="text-gray-400 text-sm mt-1">Esto puede tomar unos segundos</p>
        </div>
    );
}
