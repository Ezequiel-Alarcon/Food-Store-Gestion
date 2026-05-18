import { useState } from 'react';
import { Payment } from '@mercadopago/sdk-react';
import { useCreatePago } from '../../entities/pago/queries';
import { useUIStore } from '../../stores/uiStore';
import type { PaymentFormProps } from './types';

function BrickErrorFallback({ error }: { error: Error }) {
    return (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <p className="font-medium">No se pudo cargar el formulario de pago</p>
            <p className="text-sm mt-1">{error.message || 'Intentá de nuevo más tarde.'}</p>
        </div>
    );
}

export function PaymentForm({ pedidoId, amount, onSuccess, onError }: PaymentFormProps) {
    const [brickError, setBrickError] = useState<Error | null>(null);
    const { mutateAsync: createPago, isPending } = useCreatePago();
    const addToast = useUIStore((s) => s.addToast);

    if (brickError) {
        return <BrickErrorFallback error={brickError} />;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleSubmit = async (formData: any) => {
        try {
            const paymentType = formData?.paymentType as string | undefined;
            const data = formData?.formData;

            // Wallet / Credits — el brick redirige a MercadoPago, onSubmit no debería llamarse
            if (paymentType === 'wallet_purchase' || paymentType === 'onboarding_credits') {
                addToast('info', 'Redirigiendo a MercadoPago...');
                return;
            }

            // Ticket (Rapipago / Pago Fácil)
            if (paymentType === 'ticket') {
                const response = await createPago({
                    pedido_id: pedidoId,
                    payment_method_id: data?.payment_method_id || 'rapipago',
                });
                onSuccess(response);
                return;
            }

            // Card (creditCard / debitCard)
            const token = data?.token as string | undefined;
            if (!token) {
                addToast('error', 'No se pudo tokenizar la tarjeta. Intentá de nuevo.');
                return;
            }

            const response = await createPago({
                pedido_id: pedidoId,
                payment_method_id: data?.payment_method_id || '',
                token,
                installments: data?.installments ? Number(data.installments) : 1,
                issuer_id: data?.issuer_id || undefined,
            });

            onSuccess(response);
        } catch (err) {
            const error = err instanceof Error ? err : new Error('Error al procesar el pago');
            addToast('error', error.message || 'Error al procesar el pago');
            onError(error);
        }
    };

    const handleBrickError = (error: unknown) => {
        const err = error instanceof Error ? error : new Error('Error en el formulario de pago');
        setBrickError(err);
        addToast('error', 'Error en el formulario de pago. Intentá de nuevo.');
    };

    return (
        <div className="relative">
            {isPending && (
                <div className="absolute inset-0 bg-white/50 z-10 flex items-center justify-center rounded-lg">
                    <div className="flex flex-col items-center gap-2">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
                        <p className="text-sm text-gray-600">Procesando pago...</p>
                    </div>
                </div>
            )}
            <Payment
                initialization={{ amount }}
                customization={{
                    paymentMethods: {
                        creditCard: 'all',
                        debitCard: 'all',
                        ticket: 'all',
                        mercadoPago: 'all',
                    },
                }}
                onSubmit={handleSubmit}
                onReady={() => {}}
                onError={handleBrickError}
            />
        </div>
    );
}
