import { useBranchAddresses } from '../../entities/addresses/queries'

function formatPickup(a: {
  calle: string
  numero: string
  piso_depto: string | null
  ciudad: string
  provincia: string
  pais: string
}) {
  return `${a.calle} ${a.numero}${a.piso_depto ? `, ${a.piso_depto}` : ''} - ${a.ciudad}, ${a.provincia}, ${a.pais}`
}

export function PickupPointsPage() {
  const { data, isLoading, error } = useBranchAddresses()
  const list = data ?? []

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Puntos de retiro</h1>
      <p className="text-gray-600 mt-2">Direcciones activas de sucursales.</p>

      {isLoading ? <p className="mt-4 text-gray-600">Cargando...</p> : null}
      {error ? <p className="mt-4 text-red-600">No se pudieron cargar los puntos de retiro</p> : null}

      <div className="mt-6 space-y-3">
        {list.length === 0 ? (
          <p className="text-gray-600">No hay puntos de retiro disponibles.</p>
        ) : (
          list.map((a) => (
            <div key={a.id} className="bg-white rounded shadow p-4">
              <p className="text-sm text-gray-500">Sucursal #{a.branch_id}</p>
              <p className="font-medium mt-1">{formatPickup(a)}</p>
              {a.referencias ? <p className="text-sm text-gray-600 mt-1">{a.referencias}</p> : null}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
