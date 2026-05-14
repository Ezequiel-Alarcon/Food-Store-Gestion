import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { pagoApi } from './api';
import type { PagoCreateRequest } from './types';

export function useCreatePago() {
    const queryClient = useQueryClient();
    
    return useMutation({
        mutationFn: (payload: PagoCreateRequest) => pagoApi.create(payload),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['pago'] });
        },
    });
}

export function usePagoStatus(pedidoId: number, enabled: boolean = true) {
    return useQuery({
        queryKey: ['pago', pedidoId],
        queryFn: () => pagoApi.getByPedidoId(pedidoId),
        enabled: enabled && !!pedidoId,
        refetchInterval: (query) => {
            const status = query.state.data?.status;
            if (status === 'pending' || status === 'in_process') {
                return 3000;
            }
            return false;
        },
    });
}

export function useRetryPago() {
    const queryClient = useQueryClient();
    
    return useMutation({
        mutationFn: (pedidoId: number) => pagoApi.retry(pedidoId),
        onSuccess: (_, pedidoId) => {
            queryClient.invalidateQueries({ queryKey: ['pago', pedidoId] });
        },
    });
}
