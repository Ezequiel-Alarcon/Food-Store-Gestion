import { type ProductoCatalogo } from '../../entities/producto'

interface ProductCardProps {
  product: ProductoCatalogo
  onAddToCart: () => void
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const placeholderImage =
    'https://placehold.co/400x300/e2e8f0/64748b?text=Sin+Imagen'

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col hover:shadow-md transition-shadow">
      {/* Imagen */}
      <div className="h-48 bg-gray-100 overflow-hidden">
        <img
          src={product.imagen_url || placeholderImage}
          alt={product.nombre}
          className="w-full h-full object-cover"
          onError={(e) => {
            (e.target as HTMLImageElement).src = placeholderImage
          }}
        />
      </div>

      {/* Contenido */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
          {product.nombre}
        </h3>

        {product.descripcion && (
          <p className="text-sm text-gray-500 mb-3 line-clamp-2">
            {product.descripcion}
          </p>
        )}

        {/* Categorías */}
        {product.categorias.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {product.categorias.map((cat) => (
              <span
                key={cat.id}
                className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full"
              >
                {cat.nombre}
              </span>
            ))}
          </div>
        )}

        {/* Precio y stock */}
        <div className="mt-auto flex items-center justify-between pt-3 border-t border-gray-100">
          <span className="text-xl font-bold text-indigo-600">
            ${product.precio.toFixed(2)}
          </span>
          {!product.disponible ? (
            <span className="text-xs text-red-500 font-medium">Agotado</span>
          ) : (
            <button
              onClick={onAddToCart}
              className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Agregar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
