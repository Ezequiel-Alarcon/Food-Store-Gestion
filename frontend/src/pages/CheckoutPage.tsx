import { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AddressSelector } from '../features/checkout/AddressSelector';
import { CheckoutSummary } from '../features/checkout/CheckoutSummary';
import { PaymentForm } from '../features/checkout/CardPaymentForm';
import { PaymentResult } from '../features/checkout/PaymentResult';
import { useCartStore } from '../stores/cartStore';
import { usePaymentStore } from '../stores/paymentStore';
import { useUIStore } from '../stores/uiStore';
import { pedidoApi } from '../entities/pedido/api';
import { useQuery } from '@tanstack/react-query';
import type { PagoResponse } from '../entities/pago';

const STEPS = ['Dirección', 'Resumen', 'Pago', 'Resultado'] as const;

export default function CheckoutPage() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const pedidoIdParam = searchParams.get('pedido');
    const pedidoId = pedidoIdParam ? parseInt(pedidoIdParam, 10) : null;

    const items = useCartStore((s) => s.items);
    const clearCart = useCartStore((s) => s.clearCart);
    const addToast = useUIStore((s) => s.addToast);
    const { resetPayment, updatePaymentStatus, startCheckout } = usePaymentStore();

    // Obtener datos del pedido desde el backend
    const { data: pedido, isLoading: isPedidoLoading, isError: isPedidoError } = useQuery({
        queryKey: ['pedido', pedidoId],
        queryFn: () => pedidoApi.getById(pedidoId!),
        enabled: !!pedidoId && !isNaN(pedidoId),
        retry: 1,
    });

    const [currentStep, setCurrentStep] = useState(1);
    const [selectedAddressId, setSelectedAddressId] = useState<number | null>(null);
    const [pagoResponse, setPagoResponse] = useState<PagoResponse | null>(null);

    useEffect(() => {
        if (!pedidoId || isNaN(pedidoId)) {
            addToast('error', 'No se encontró el pedido. Agregá productos al carrito primero.');
            navigate('/carrito', { replace: true });
        }
    }, [pedidoId, navigate, addToast]);

    // Si el pedido no existe en backend, redirigir
    useEffect(() => {
        if (isPedidoError || (!isPedidoLoading && !pedido)) {
            addToast('error', 'El pedido no fue encontrado. Creá uno nuevo desde el carrito.');
            navigate('/carrito', { replace: true });
        }
    }, [isPedidoError, isPedidoLoading, pedido, navigate, addToast]);

    // FIXED: No redirigir por carrito vacío — el checkout obtiene datos del pedido desde backend

    // FIXED: useBlocker was crashing the app because it requires a Data Router (createBrowserRouter).
    // Con BrowserRouter tira un invariant error que rompe todo el árbol de React (pantalla blanca).
    // Se removió el useBlocker temporalmente.


    useEffect(() => {
        return () => {
            resetPayment();
        };
    }, [resetPayment]);

    const handlePaymentSuccess = useCallback((response: PagoResponse) => {
        setPagoResponse(response);
        updatePaymentStatus(response.status, response.status_detail ?? undefined);
        if (response.status === 'approved') {
            clearCart(); // Solo limpiar carrito cuando el pago es aprobado
        }
        setCurrentStep(4);
    }, [updatePaymentStatus, clearCart]);

    const handlePaymentError = useCallback((error: Error) => {
        addToast('error', error.message || 'Error al procesar el pago');
    }, [addToast]);

    const handleRetry = useCallback(() => {
        setPagoResponse(null);
        setCurrentStep(3);
    }, []);

    const totalInCents = useMemo(() => {
        if (pedido?.total && pedido.total > 0) return Math.round(pedido.total * 100);
        return 0;
    }, [pedido]);

    const hasValidAmount = totalInCents > 0;

    const progressPercent = ((currentStep - 1) / (STEPS.length - 1)) * 100;

    if (!pedidoId || isNaN(pedidoId)) return null;

    if (isPedidoLoading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto" />
                    <p className="mt-4 text-gray-500">Cargando pedido...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <nav aria-label="Progreso del checkout" className="mb-8">
                    <ol className="flex items-center">
                        {STEPS.map((step, index) => {
                            const stepNum = index + 1;
                            const isCompleted = stepNum < currentStep;
                            const isCurrent = stepNum === currentStep;

                            return (
                                <li key={step} className={`flex items-center ${index < STEPS.length - 1 ? 'flex-1' : ''}`}>
                                    <div className="flex flex-col items-center">
                                        <div
                                            className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium transition-colors ${
                                                isCompleted
                                                    ? 'bg-indigo-600 text-white'
                                                    : isCurrent
                                                    ? 'bg-indigo-600 text-white ring-4 ring-indigo-100'
                                                    : 'bg-gray-200 text-gray-600'
                                            }`}
                                            aria-current={isCurrent ? 'step' : undefined}
                                        >
                                            {isCompleted ? '✓' : stepNum}
                                        </div>
                                        <span className={`mt-1 text-xs hidden sm:block ${
                                            isCurrent ? 'text-indigo-600 font-medium' : 'text-gray-500'
                                        }`}>
                                            {step}
                                        </span>
                                    </div>
                                    {index < STEPS.length - 1 && (
                                        <div className="flex-1 mx-2 h-0.5 bg-gray-200">
                                            <div
                                                className="h-full bg-indigo-600 transition-all duration-300"
                                                style={{ width: isCompleted ? '100%' : '0%' }}
                                            />
                                        </div>
                                    )}
                                </li>
                            );
                        })}
                    </ol>
                    <div className="mt-2 sm:hidden">
                        <div className="bg-gray-200 rounded-full h-1">
                            <div
                                className="bg-indigo-600 h-1 rounded-full transition-all duration-300"
                                style={{ width: `${progressPercent}%` }}
                            />
                        </div>
                    </div>
                </nav>

                <div className="bg-white rounded-lg shadow-sm p-6">
                    {currentStep === 1 && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Dirección de entrega</h2>
                            <AddressSelector
                                selectedAddressId={selectedAddressId}
                                onSelect={setSelectedAddressId}
                            />
                            <div className="mt-6">
                                <button
                                    onClick={() => {
                                        if (!selectedAddressId) {
                                            addToast('error', 'Seleccioná una dirección de entrega');
                                            return;
                                        }
                                        setCurrentStep(2);
                                    }}
                                    disabled={!selectedAddressId}
                                    className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
                                >
                                    Continuar
                                </button>
                            </div>
                        </div>
                    )}

                    {currentStep === 2 && selectedAddressId && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Resumen del pedido</h2>
                            <CheckoutSummary
                                pedidoId={pedidoId}
                                selectedAddressId={selectedAddressId}
                                onConfirm={() => {
                                    startCheckout(pedidoId);
                                    setCurrentStep(3);
                                }}
                                pedidoItems={pedido?.items}
                                pedidoTotal={pedido?.total}
                            />
                        </div>
                    )}

                    {currentStep === 3 && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Método de pago</h2>
                            {!hasValidAmount ? (
                                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                                    <p className="font-medium">No se puede procesar el pago</p>
                                    <p className="text-sm mt-1">El pedido no tiene un total válido. Volvé al carrito y reintentá.</p>
                                </div>
                            ) : (
                                <PaymentForm
                                    pedidoId={pedidoId}
                                    amount={totalInCents}
                                    onSuccess={handlePaymentSuccess}
                                    onError={handlePaymentError}
                                />
                            )}
                        </div>
                    )}

                    {currentStep === 4 && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Resultado del pago</h2>
                            <PaymentResult
                                pagoResponse={pagoResponse}
                                pedidoId={pedidoId}
                                onRetry={handleRetry}
                            />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
