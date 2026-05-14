/**
 * Tabla de ranking de productos más vendidos.
 */
import type { TopProductEntry } from '../types'

interface TopProductsTableProps {
  data: TopProductEntry[]
  isLoading?: boolean
}

/**
 * Tabla que muestra el top 10 de productos más vendidos
 * con su cantidad de unidades vendidas.
 */
export function TopProductsTable({ data, isLoading }: TopProductsTableProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-48 mb-4" />
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-100 rounded" />
          ))}
        </div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Productos</h3>
        <div className="py-8 text-center text-gray-500">
          <p>No hay datos de productos vendidos</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Productos Más Vendidos</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
                #
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Producto
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ventas
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((product, index) => (
              <tr key={product.producto_id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-400">
                  {index + 1}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900">
                  {product.nombre}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900 text-right font-medium">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                    {product.cantidad_vendida.toLocaleString('es-AR')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}