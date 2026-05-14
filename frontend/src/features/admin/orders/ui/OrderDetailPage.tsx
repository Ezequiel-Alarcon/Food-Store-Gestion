import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { pedidoAdminApi } from '../../../../entities/pedido-admin/api'

const ESTADO_COLORS: Record<string, string> = {
  PENDIENTE: 'bg-yellow-100 text-yellow-800',
  CONFIRMADO: 'bg-blue-100 text-blue-800',
  EN_PREP: 'bg-purple-100 text-purple-800',
  EN_CAMINO: 'bg-indigo-100 text-indigo-800',
  ENTREGADO: 'bg-green-100 text-green-800',
  CANCELADO: 'bg-red-100 text-red-800',
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
  }).format(amount)
}

function OrderInfoCard({ order }: { order: any }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Información del Pedido</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-500">ID del Pedido</p>
          <p className="font-medium">#{order.id}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Estado</p>
          <span
            className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
              ESTADO_COLORS[order.estado_codigo] || 'bg-gray-100 text-gray-800'
            }`}
          >
            {order.estado_codigo}
          </span>
        </div>
        <div>
          <p className="text-sm text-gray-500">Cliente</p>
          <p className="font-medium">
            {order.cliente_nombre || ''} {order.cliente_apellido || ''}
          </p>
          <p className="text-sm text-gray-500">{order.cliente_email}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Fecha de Creación</p>
          <p className="font-medium">{formatDate(order.creado_en)}</p>
        </div>
      </div>
    </div>
  )
}

function OrderAddressCard({ order }: { order: any }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Dirección de Entrega</h3>
      <div className="space-y-2">
        <p className="text-gray-700">
          {order.direccion_calle} {order.direccion_numero}
          {order.direccion_piso_depto && `, ${order.direccion_piso_depto}`}
        </p>
        <p className="text-gray-700">
          {order.direccion_ciudad}, {order.direccion_provincia}
        </p>
        {order.direccion_codigo_postal && (
          <p className="text-gray-500">CP: {order.direccion_codigo_postal}</p>
        )}
        {order.direccion_referencias && (
          <p className="text-sm text-gray-500 mt-2">
            <span className="font-medium">Referencia:</span> {order.direccion_referencias}
          </p>
        )}
      </div>
    </div>
  )
}

function OrderItemsList({ items }: { items: any[] }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Items del Pedido</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Producto</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Cantidad</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Precio Unit.</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Subtotal</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {items.map((item) => (
              <tr key={item.id}>
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-900">{item.producto_nombre || `#${item.producto_id}`}</p>
                  {item.exclusiones && item.exclusiones.length > 0 && (
                    <p className="text-xs text-gray-500">Sin: {item.exclusiones.join(', ')}</p>
                  )}
                </td>
                <td className="px-4 py-3 text-gray-700">{item.cantidad}</td>
                <td className="px-4 py-3 text-gray-700">{formatCurrency(item.precio_unitario)}</td>
                <td className="px-4 py-3 font-medium text-gray-900">
                  {formatCurrency(item.cantidad * item.precio_unitario)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 pt-4 border-t flex justify-between">
        <div>
          <p className="text-sm text-gray-500">Costo de envío</p>
          <p className="font-medium">{formatCurrency(0)}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Total</p>
          <p className="text-xl font-bold text-gray-900">{formatCurrency(0)}</p>
        </div>
      </div>
    </div>
  )
}

function OrderTimeline({ history }: { history: any[] }) {
  if (!history || history.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Historial de Estados</h3>
        <p className="text-gray-500">No hay historial disponible</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Historial de Estados</h3>
      <div className="relative">
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />
        <div className="space-y-6">
          {history.map((item) => (
            <div key={item.id} className="relative pl-10">
              <div className="absolute left-2.5 w-3 h-3 rounded-full bg-indigo-500 border-2 border-white" />
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span
                    className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                      ESTADO_COLORS[item.estado_nuevo_codigo] || 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {item.estado_nuevo_codigo}
                  </span>
                  <span className="text-sm text-gray-500">{formatDate(item.creado_en)}</span>
                </div>
                {item.motivo && <p className="text-sm text-gray-600 mt-1">{item.motivo}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      <div className="h-48 bg-gray-200 rounded" />
      <div className="h-32 bg-gray-200 rounded" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  )
}

export function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()
  const orderId = Number(id)

  const { data: order, isLoading: orderLoading, isError: orderError } = useQuery({
    queryKey: ['admin-order', orderId],
    queryFn: () => pedidoAdminApi.getOrderById(orderId),
    enabled: !!orderId,
  })

  const { data: history } = useQuery({
    queryKey: ['admin-order-history', orderId],
    queryFn: () => pedidoAdminApi.getOrderHistory(orderId),
    enabled: !!orderId,
  })

  if (orderLoading) {
    return (
      <div className="p-6 max-w-5xl mx-auto">
        <LoadingSkeleton />
      </div>
    )
  }

  if (orderError || !order) {
    return (
      <div className="p-6 max-w-5xl mx-auto text-center">
        <p className="text-red-600 mb-4">Error al cargar el pedido</p>
        <Link to="/admin/pedidos" className="text-indigo-600 hover:text-indigo-900">
          Volver a la lista
        </Link>
      </div>
    )
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/admin/pedidos"
          className="text-indigo-600 hover:text-indigo-900 text-sm mb-2 inline-block"
        >
          ← Volver a pedidos
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">Detalle del Pedido #{order.id}</h1>
      </div>

      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <OrderInfoCard order={order} />
          <OrderAddressCard order={order} />
        </div>

        <OrderItemsList items={order.items} />

        <OrderTimeline history={history || []} />
      </div>
    </div>
  )
}