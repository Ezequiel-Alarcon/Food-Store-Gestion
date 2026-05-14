import { useMutation, useQueryClient } from '@tanstack/react-query';
import { pedidoApi } from './api';
import type { PedidoCreateRequest, PedidoDetalle } from './types';

export function useCreatePedido() {
    const queryClient = useQueryClient();
    
    return useMutation<PedidoDetalle, Error, PedidoCreateRequest>({
        mutationFn: (payload) => pedidoApi.create(payload),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['pedidos'] });
        },
    });
}
