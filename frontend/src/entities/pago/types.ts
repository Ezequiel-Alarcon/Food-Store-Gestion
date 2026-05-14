export interface PagoCreateRequest {
    pedido_id: number;
    payment_method_id: string;
    token?: string;
}

export interface PagoResponse {
    id: number;
    pedido_id: number;
    mp_payment_id: number | null;
    idempotency_key: string;
    external_reference: string;
    status: PagoStatus;
    status_detail: string | null;
    payment_method_id: string | null;
    transaction_amount: number;
    creado_en: string;
    actualizado_en: string;
}

export type PagoStatus = 'pending' | 'approved' | 'rejected' | 'in_process' | 'cancelled' | 'refunded';

export interface PedidoResumen {
    id: number;
    estado: string;
    total: number;
    creado_en: string;
}
