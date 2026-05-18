import type { PagoResponse } from '../../entities/pago';

export interface AddressSelectorProps {
    selectedAddressId: number | null;
    onSelect: (addressId: number) => void;
}

export interface CheckoutSummaryItem {
    producto_id: number
    cantidad: number
    precio_unitario: number
}

export interface CheckoutSummaryProps {
    pedidoId: number;
    selectedAddressId: number;
    onConfirm: () => void;
    pedidoItems?: CheckoutSummaryItem[]
    pedidoTotal?: number
}

export interface CardPaymentFormProps {
    pedidoId: number;
    amount: number;
    onSuccess: (response: PagoResponse) => void;
    onError: (error: Error) => void;
}

export interface PaymentResultProps {
    pagoResponse: PagoResponse | null;
    pedidoId: number;
    onRetry: () => void;
}
