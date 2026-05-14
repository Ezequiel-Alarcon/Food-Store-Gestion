import { useState, useEffect, useCallback } from 'react'
import { productoApi, type ProductoCatalogo } from '../entities/producto'
import { ProductCard } from '../features/cart/ProductCard'
import { IngredientsModal } from '../features/cart/IngredientsModal'
import { useCartStore, type Producto } from '../stores/cartStore'
import { useUIStore } from '../stores/uiStore'

const PAGE_SIZE = 12

export function CatalogPage() {
  const [products, setProducts] = useState<ProductoCatalogo[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  // Modal de ingredientes
  const [ingredientsModal, setIngredientsModal] = useState<{
    open: boolean
    productId: number
    productName: string
    ingredients: Array<{ id: number; nombre: string }>
  } | null>(null)

  const addItem = useCartStore((s) => s.addItem)
  const addToast = useUIStore((s) => s.addToast)

  const fetchProducts = useCallback(async (currentPage: number) => {
    setLoading(true)
    setError(null)
    try {
      const data = await productoApi.getCatalogo({
        disponibles: true,
        page: currentPage,
        size: PAGE_SIZE,
      })
      setProducts(data.items)
      setTotal(data.total)
    } catch {
      setError('No se pudieron cargar los productos. Intentá de nuevo.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchProducts(page)
  }, [page, fetchProducts])

  const totalPages = Math.ceil(total / PAGE_SIZE)

  const mapToCartProduct = (p: ProductoCatalogo): Producto => ({
    id: p.id,
    nombre: p.nombre,
    precio: p.precio,
    imagenUrl: p.imagen_url || '',
  })

  const handleAddToCart = async (product: ProductoCatalogo) => {
    try {
      const detalle = await productoApi.getById(product.id)
      if (detalle.ingredientes && detalle.ingredientes.length > 0) {
        setIngredientsModal({
          open: true,
          productId: product.id,
          productName: product.nombre,
          ingredients: detalle.ingredientes,
        })
      } else {
        addItem(mapToCartProduct(product), 1)
        addToast('success', `${product.nombre} agregado al carrito`)
      }
    } catch {
      // Si falla el detalle, agregar sin ingredientes
      addItem(mapToCartProduct(product), 1)
      addToast('success', `${product.nombre} agregado al carrito`)
    }
  }

  const handleIngredientsConfirm = (excludedIds: number[]) => {
    if (!ingredientsModal) return
    const product = products.find((p) => p.id === ingredientsModal.productId)
    if (product) {
      addItem(mapToCartProduct(product), 1, excludedIds)
      addToast('success', `${product.nombre} agregado al carrito`)
    }
    setIngredientsModal(null)
  }

  // Filtrar productos localmente por el search term
  const filteredProducts = searchTerm.trim()
    ? products.filter(
        (p) =>
          p.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
          (p.descripcion && p.descripcion.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    : products

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Catálogo de Productos</h1>

      {/* Barra de búsqueda (filtrado local) */}
      <div className="mb-8">
        <div className="flex gap-2 max-w-md">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar productos..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="px-3 py-2 text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Estados */}
      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {!loading && !error && filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">
            {searchTerm ? 'No se encontraron productos con ese término.' : 'No hay productos disponibles.'}
          </p>
        </div>
      )}

      {/* Grid de productos */}
      {!loading && !error && filteredProducts.length > 0 && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={() => handleAddToCart(product)}
              />
            ))}
          </div>

          {/* Paginación — oculta mientras se busca */}
          {!searchTerm && totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-8">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                ← Anterior
              </button>
              <span className="text-sm text-gray-600">
                Página {page} de {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-3 py-1 rounded border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Siguiente →
              </button>
            </div>
          )}
        </>
      )}

      {/* Modal de ingredientes */}
      {ingredientsModal && (
        <IngredientsModal
          productName={ingredientsModal.productName}
          ingredients={ingredientsModal.ingredients}
          onConfirm={handleIngredientsConfirm}
          onClose={() => setIngredientsModal(null)}
        />
      )}
    </div>
  )
}
