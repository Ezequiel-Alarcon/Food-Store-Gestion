import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { productoApi } from '../entities/producto'
import type { ProductoDetalle } from '../entities/producto/types'
import { useCartStore, type Producto } from '../stores/cartStore'
import { useUIStore } from '../stores/uiStore'

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const productId = Number(id)

  const {
    data: product,
    isLoading,
    isError,
  } = useQuery<ProductoDetalle>({
    queryKey: ['producto', productId],
    queryFn: () => productoApi.getById(productId),
    enabled: !isNaN(productId),
  })

  const addItem = useCartStore((s) => s.addItem)
  const addToast = useUIStore((s) => s.addToast)

  const placeholderImage =
    'https://placehold.co/600x400/e2e8f0/64748b?text=Sin+Imagen'

  const mapToCartProduct = (p: ProductoDetalle): Producto => ({
    id: p.id,
    nombre: p.nombre,
    precio: p.precio,
    imagenUrl: p.imagen_url || '',
  })

  const handleAddToCart = () => {
    if (!product) return
    addItem(mapToCartProduct(product), 1)
    addToast('success', `${product.nombre} agregado al carrito`)
  }

  if (isNaN(productId)) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          ID de producto inválido.
        </div>
        <Link
          to="/productos"
          className="inline-block mt-4 text-indigo-600 hover:text-indigo-800 font-medium"
        >
          ← Volver al catálogo
        </Link>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    )
  }

  if (isError || !product) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          No se pudo cargar el producto.
        </div>
        <Link
          to="/productos"
          className="inline-block mt-4 text-indigo-600 hover:text-indigo-800 font-medium"
        >
          ← Volver al catálogo
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Link
        to="/productos"
        className="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800 font-medium mb-6"
      >
        ← Volver al catálogo
      </Link>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="md:flex">
          {/* Imagen */}
          <div className="md:w-1/2 h-80 md:h-auto bg-gray-100">
            <img
              src={product.imagen_url || placeholderImage}
              alt={product.nombre}
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = placeholderImage
              }}
            />
          </div>

          {/* Detalle */}
          <div className="md:w-1/2 p-6 md:p-8 flex flex-col">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              {product.nombre}
            </h1>

            {product.descripcion && (
              <p className="text-gray-600 mb-4">{product.descripcion}</p>
            )}

            <div className="text-3xl font-bold text-indigo-600 mb-4">
              ${product.precio.toFixed(2)}
            </div>

            {/* Stock */}
            <div className="mb-4">
              {product.disponible ? (
                <span className="inline-flex items-center gap-1 text-sm text-green-700 bg-green-50 px-3 py-1 rounded-full">
                  <span className="w-2 h-2 bg-green-500 rounded-full" />
                  Disponible
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-sm text-red-700 bg-red-50 px-3 py-1 rounded-full">
                  <span className="w-2 h-2 bg-red-500 rounded-full" />
                  Agotado
                </span>
              )}
            </div>

            {/* Categorías */}
            {product.categorias.length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Categorías
                </h3>
                <div className="flex flex-wrap gap-1">
                  {product.categorias.map((cat) => (
                    <span
                      key={cat.id}
                      className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full"
                    >
                      {cat.nombre}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Ingredientes */}
            {product.ingredientes.length > 0 && (
              <div className="mb-6">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Ingredientes
                </h3>
                <div className="flex flex-wrap gap-1">
                  {product.ingredientes.map((ing) => (
                    <span
                      key={ing.id}
                      className={`text-xs px-2 py-0.5 rounded-full ${
                        ing.es_alergeno
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {ing.nombre}
                      {ing.es_alergeno && ' ⚠'}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Botón agregar */}
            <div className="mt-auto pt-6 border-t border-gray-100">
              <button
                onClick={handleAddToCart}
                disabled={!product.disponible}
                className="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {product.disponible
                  ? 'Agregar al carrito'
                  : 'Producto no disponible'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
