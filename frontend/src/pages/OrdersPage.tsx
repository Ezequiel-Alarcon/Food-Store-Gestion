import { useState, useEffect, useCallback } from 'react'
import { pedidoApi, type PedidoListItem, type PedidoDetalle } from '../entities/pedido'

const ESTADOS = ['PENDIENTE', 'CONFIRMADO', 'EN_PREP', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO']

const ESTADO_COLORS: Record<string, string> = {
  PENDIENTE: 'bg-yellow-100 text-yellow-800',
  CONFIRMADO: 'bg-green-100 text-green-800',
  EN_PREP: 'bg-blue-100 text-blue-800',
  EN_CAMINO: 'bg-orange-100 text-orange-800',
  ENTREGADO: 'bg-emerald-100 text-emerald-800',
  CANCELADO: 'bg-red-100 text-red-800',
}

const ESTADO_LABELS: Record<string, string> = {
  PENDIENTE: 'Pendiente',
  CONFIRMADO: 'Confirmado',
  EN_PREP: 'En preparación',
  EN_CAMINO: 'En camino',
  ENTREGADO: 'Entregado',
  CANCELADO: 'Cancelado',
}

export function OrdersPage() {
  const [orders, setOrders] = useState<PedidoListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)
  const [filterEstado, setFilterEstado] = useState('')

  // Detalle drawer
  const [selectedOrder, setSelectedOrder] = useState<PedidoDetalle | null>(null)
  const [loadingDetail, setLoadingDetail] = useState(false)

  const fetchOrders = useCallback(async (p: number, estado: string) => {
    setLoading(true)
    setError(null)
    try {
      const data = await pedidoApi.getMisPedidos({ page: p, size: 10, estado: estado || undefined })
      setOrders(data.items)
      setTotalPages(data.pages)
      setTotal(data.total)
    } catch {
      setError('No se pudieron cargar los pedidos.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchOrders(page, filterEstado) }, [page, filterEstado, fetchOrders])

  const handleFilterChange = (estado: string) => {
    setFilterEstado(estado)
    setPage(1)
  }

  const openDetail = async (id: number) => {
    setLoadingDetail(true)
    setError(null)
    setSelectedOrder(null)
    try {
      const detail = await pedidoApi.getById(id)
      setSelectedOrder(detail)
    } catch {
      setError('No se pudo cargar el detalle.')
    } finally {
      setLoadingDetail(false)
    }
  }

  const formatDate = (d: string) => new Date(d).toLocaleDateString('es-AR', { day: 'numeric', month: 'short', year: 'numeric' })
  const formatCurrency = (n: number) => `$${n.toFixed(2)}`

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Mis Pedidos</h1>

      {/* Filtro por estado */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => handleFilterChange('')}
          className={`px-3 py-1.5 text-xs font-medium rounded-full transition-colors ${!filterEstado ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          Todos{total > 0 ? ` (${total})` : ''}
        </button>
        {ESTADOS.map((e) => (
          <button
            key={e}
            onClick={() => handleFilterChange(e)}
            className={`px-3 py-1.5 text-xs font-medium rounded-full transition-colors ${filterEstado === e ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
          >
            {ESTADO_LABELS[e]}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600" />
        </div>
      )}

      {/* Error */}
      {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">{error}</div>}

      {/* Empty */}
      {!loading && !error && orders.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <p className="text-gray-500 text-lg">No tenés pedidos todavía</p>
          <p className="text-gray-400 mt-1">Tus pedidos aparecerán acá cuando hagas uno.</p>
        </div>
      )}

      {/* Orders list */}
      {!loading && !error && orders.length > 0 && (
        <>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            {/* Desktop table */}
            <table className="hidden sm:table w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pedido</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {orders.map((o) => (
                  <tr key={o.id} onClick={() => openDetail(o.id)} className="hover:bg-gray-50 cursor-pointer transition-colors">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">#{o.id}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">{formatDate(o.created_at)}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex px-2 py-0.5 text-xs font-medium rounded-full ${ESTADO_COLORS[o.estado_codigo] || 'bg-gray-100 text-gray-700'}`}>
                        {ESTADO_LABELS[o.estado_codigo] || o.estado_codigo}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm font-semibold text-gray-900 text-right">{formatCurrency(o.total)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Mobile cards */}
            <div className="sm:hidden divide-y divide-gray-100">
              {orders.map((o) => (
                <div key={o.id} onClick={() => openDetail(o.id)} className="p-4 hover:bg-gray-50 cursor-pointer">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-sm font-semibold text-gray-900">Pedido #{o.id}</span>
                    <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${ESTADO_COLORS[o.estado_codigo] || 'bg-gray-100'}`}>
                      {ESTADO_LABELS[o.estado_codigo] || o.estado_codigo}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">{formatDate(o.created_at)}</span>
                    <span className="font-semibold text-gray-900">{formatCurrency(o.total)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-6">
              <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 hover:bg-gray-50 text-sm">← Anterior</button>
              <span className="text-sm text-gray-600">Página {page} de {totalPages}</span>
              <button onClick={() => setPage((p) => Math.min(totalPages, p + 1))} disabled={page === totalPages} className="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 hover:bg-gray-50 text-sm">Siguiente →</button>
            </div>
          )}
        </>
      )}

      {/* Detail drawer */}
      {selectedOrder && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="absolute inset-0 bg-black/40" onClick={() => setSelectedOrder(null)} />
          <div className="relative w-full max-w-lg bg-white shadow-xl h-full overflow-y-auto">
            {loadingDetail ? (
              <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>
            ) : (
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">Pedido #{selectedOrder.id}</h2>
                    <span className={`inline-flex mt-1 px-2 py-0.5 text-xs font-medium rounded-full ${ESTADO_COLORS[selectedOrder.estado_codigo] || 'bg-gray-100 text-gray-700'}`}>
                      {ESTADO_LABELS[selectedOrder.estado_codigo]}
                    </span>
                  </div>
                  <button onClick={() => setSelectedOrder(null)} className="text-gray-400 hover:text-gray-600 p-1">✕</button>
                </div>

                {/* Items */}
                <div className="mb-6">
                  <h3 className="text-sm font-semibold text-gray-700 mb-3">Productos</h3>
                  <div className="space-y-2">
                    {selectedOrder.items.map((item) => (
                      <div key={item.id} className="flex justify-between items-center bg-gray-50 rounded-lg p-3">
                        <div>
                          <p className="text-sm font-medium text-gray-900">Producto #{item.producto_id}</p>
                          <p className="text-xs text-gray-500">{item.cantidad} x {formatCurrency(item.precio_unitario)}</p>
                        </div>
                        <span className="text-sm font-semibold text-gray-900">{formatCurrency(item.cantidad * item.precio_unitario)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Dirección */}
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Dirección de entrega</h3>
                  <p className="text-sm text-gray-600">
                    {selectedOrder.direccion_calle} {selectedOrder.direccion_numero}
                    {selectedOrder.direccion_piso_depto ? `, ${selectedOrder.direccion_piso_depto}` : ''}
                  </p>
                  <p className="text-sm text-gray-600">{selectedOrder.direccion_ciudad}, {selectedOrder.direccion_provincia}</p>
                </div>

                {/* Totals */}
                <div className="border-t pt-4 space-y-1">
                  <div className="flex justify-between text-sm"><span className="text-gray-500">Subtotal</span><span className="text-gray-900">{formatCurrency(selectedOrder.total - selectedOrder.costo_envio)}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-gray-500">Envío</span><span className="text-gray-900">{formatCurrency(selectedOrder.costo_envio)}</span></div>
                  <div className="flex justify-between text-base font-bold pt-2 border-t"><span className="text-gray-900">Total</span><span className="text-indigo-600">{formatCurrency(selectedOrder.total)}</span></div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
