import { api } from '../../lib/api';
import type { PagoCreateRequest, PagoResponse } from './types';

export const pagoApi = {
    create: async (payload: PagoCreateRequest): Promise<PagoResponse> => {
        const res = await api.post<PagoResponse>('/pagos/crear', payload);
        return res.data;
    },

    getByPedidoId: async (pedidoId: number): Promise<PagoResponse> => {
        const res = await api.get<PagoResponse>(`/pagos/${pedidoId}`);
        return res.data;
    },

    retry: async (pedidoId: number): Promise<PagoResponse> => {
        const res = await api.post<PagoResponse>(`/pagos/${pedidoId}/reintentar`);
        return res.data;
    },
};
