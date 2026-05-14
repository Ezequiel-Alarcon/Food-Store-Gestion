import { useEffect } from 'react';
import { useUserAddresses } from '../../entities/addresses/queries';
import type { UserAddress } from '../../entities/addresses/types';
import type { AddressSelectorProps } from './types';

export function AddressSelector({ selectedAddressId, onSelect }: AddressSelectorProps) {
    const { data: addresses, isLoading, isError, refetch } = useUserAddresses();

    useEffect(() => {
        if (addresses && selectedAddressId === null) {
            const defaultAddr = addresses.find((a: UserAddress) => a.is_default);
            if (defaultAddr) {
                onSelect(defaultAddr.id);
            }
        }
    }, [addresses, selectedAddressId, onSelect]);

    if (isLoading) {
        return (
            <div className="space-y-3" role="status" aria-label="Cargando direcciones">
                {[1, 2, 3].map(i => (
                    <div key={i} className="animate-pulse bg-white rounded-lg shadow-sm p-4">
                        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                        <div className="h-3 bg-gray-200 rounded w-1/2" />
                    </div>
                ))}
            </div>
        );
    }

    if (isError) {
        return (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                <p className="font-medium">No se pudieron cargar las direcciones</p>
                <button onClick={() => refetch()} className="text-red-600 underline mt-1 text-sm">
                    Intentar de nuevo
                </button>
            </div>
        );
    }

    if (!addresses || addresses.length === 0) {
        return (
            <div className="text-center py-8">
                <p className="text-gray-500 mb-4">No tenés direcciones guardadas</p>
                <a href="/direcciones" className="inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                    Agregar dirección
                </a>
            </div>
        );
    }

    return (
        <div className="space-y-3" role="radiogroup" aria-label="Seleccioná una dirección de entrega">
            {addresses.map((addr: UserAddress) => (
                <label
                    key={addr.id}
                    className={`block cursor-pointer rounded-lg border-2 p-4 transition-colors ${
                        selectedAddressId === addr.id
                            ? 'border-indigo-500 bg-indigo-50'
                            : 'border-gray-200 bg-white hover:border-gray-300'
                    }`}
                >
                    <input
                        type="radio"
                        name="address"
                        value={addr.id}
                        checked={selectedAddressId === addr.id}
                        onChange={() => onSelect(addr.id)}
                        className="sr-only"
                    />
                    <div className="flex items-start gap-3">
                        <div className={`mt-0.5 h-4 w-4 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                            selectedAddressId === addr.id ? 'border-indigo-500' : 'border-gray-300'
                        }`}>
                            {selectedAddressId === addr.id && (
                                <div className="h-2 w-2 rounded-full bg-indigo-500" />
                            )}
                        </div>
                        <div className="min-w-0">
                            <p className="font-medium text-gray-900 truncate">
                                {addr.calle} {addr.numero}
                                {addr.is_default && (
                                    <span className="ml-2 inline-flex items-center rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700">
                                        Principal
                                    </span>
                                )}
                            </p>
                            <p className="text-sm text-gray-500">
                                {[addr.ciudad, addr.provincia].filter(Boolean).join(', ')}
                            </p>
                            {addr.referencias && (
                                <p className="text-xs text-gray-400 mt-0.5 truncate">{addr.referencias}</p>
                            )}
                        </div>
                    </div>
                </label>
            ))}
        </div>
    );
}
