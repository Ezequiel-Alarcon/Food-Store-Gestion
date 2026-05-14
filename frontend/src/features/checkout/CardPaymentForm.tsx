import { useState } from 'react';
import { CardPayment } from '@mercadopago/sdk-react';
import { useCreatePago } from '../../entities/pago/queries';
import { useUIStore } from '../../stores/uiStore';
import type { CardPaymentFormProps } from './types';

function BrickErrorFallback({ error }: { error: Error }) {
    return (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <p className="font-medium">No se pudo cargar el formulario de pago</p>
            <p className="text-sm mt-1">{error.message || 'Intentá de nuevo más tarde.'}</p>
        </div>
    );
}

export function CardPaymentForm({ pedidoId, amount, onSuccess, onError }: CardPaymentFormProps) {
    const [brickError, setBrickError] = useState<Error | null>(null);
    const { mutateAsync: createPago, isPending } = useCreatePago();
    const addToast = useUIStore((s) => s.addToast);

    if (brickError) {
        return <BrickErrorFallback error={brickError} />;
    }

    // MP SDK onSubmit receives ICardPaymentFormData — token and payment_method_id
    // are direct properties. We use a permissive type to match the SDK signature.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleSubmit = async (formData: any) => {
        try {
            const token = formData?.token as string | undefined;
            const paymentMethodId = formData?.payment_method_id as string | undefined;

            if (!token) {
                addToast('error', 'No se pudo tokenizar la tarjeta. Intentá de nuevo.');
                return;
            }

            const response = await createPago({
                pedido_id: pedidoId,
                payment_method_id: paymentMethodId || '',
                token,
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
            <CardPayment
                initialization={{ amount }}
                onSubmit={handleSubmit}
                onReady={() => {
                    // Brick is ready — could hide loading state here
                }}
                onError={handleBrickError}
            />
        </div>
    );
}
