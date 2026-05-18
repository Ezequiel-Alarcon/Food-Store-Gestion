import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { type ProductoCatalogo } from '../entities/producto'
import { api } from '../lib/api'
import type { PaginatedResponse } from '../entities/producto/types'
import { ProductCard } from '../features/cart/ProductCard'
import { useCartStore, type Producto } from '../stores/cartStore'
import { useUIStore } from '../stores/uiStore'

const PAGE_SIZE = 12

export function CatalogPage() {
  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 300)
    return () => clearTimeout(timer)
  }, [searchTerm])

  const { data, isLoading, isError } = useQuery({
    queryKey: ['catalogo', page, debouncedSearch],
    queryFn: () =>
      api
        .get<PaginatedResponse<ProductoCatalogo>>('/productos/catalogo', {
          params: {
            skip: (page - 1) * PAGE_SIZE,
            limit: PAGE_SIZE,
            disponibles: true,
            search: debouncedSearch || undefined,
          },
        })
        .then((r) => r.data),
  })

  const products = data?.items ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / PAGE_SIZE)

  const addItem = useCartStore((s) => s.addItem)
  const addToast = useUIStore((s) => s.addToast)

  const mapToCartProduct = (p: ProductoCatalogo): Producto => ({
    id: p.id,
    nombre: p.nombre,
    precio: p.precio,
    imagenUrl: p.imagen_url || '',
  })

  const handleAddToCart = (product: ProductoCatalogo) => {
    addItem(mapToCartProduct(product), 1)
    addToast('success', `${product.nombre} agregado al carrito`)
  }

  const isSearchPending = searchTerm !== debouncedSearch

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Catálogo de Productos</h1>

      {/* Barra de búsqueda */}
      <div className="mb-8">
        <div className="flex gap-2 max-w-md">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value)
              setPage(1)
            }}
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
        {isSearchPending && (
          <p className="text-sm text-gray-400 mt-1">Buscando...</p>
        )}
      </div>

      {/* Estados */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
        </div>
      )}

      {isError && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          No se pudieron cargar los productos. Intentá de nuevo.
        </div>
      )}

      {!isLoading && !isError && products.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">
            {debouncedSearch ? 'No se encontraron productos con ese término.' : 'No hay productos disponibles.'}
          </p>
        </div>
      )}

      {/* Grid de productos */}
      {!isLoading && !isError && products.length > 0 && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={() => handleAddToCart(product)}
              />
            ))}
          </div>

          {/* Paginación — oculta mientras se busca */}
          {!debouncedSearch && totalPages > 1 && (
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
    </div>
  )
}
