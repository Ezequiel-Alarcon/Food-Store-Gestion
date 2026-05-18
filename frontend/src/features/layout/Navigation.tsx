import { Link } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import { useCartStore } from '../../stores/cartStore'
import { useUIStore } from '../../stores/uiStore'

// Definición de menú por rol
const MENU_BY_ROLE: Record<string, Array<{ label: string; href: string }>> = {
  CLIENT: [
    { label: 'Productos', href: '/productos' },
    { label: 'Mis Pedidos', href: '/pedidos' },
    { label: 'Mis Direcciones', href: '/direcciones' },
    { label: 'Mi Perfil', href: '/perfil' },
    { label: 'Puntos de Retiro', href: '/puntos-retiro' },
  ],
  STOCK: [
    { label: 'Productos', href: '/productos' },
    { label: 'Gestión de Stock', href: '/admin/stock' },
  ],
  PEDIDOS: [
    { label: 'Productos', href: '/productos' },
    { label: 'Gestión de Pedidos', href: '/admin/pedidos' },
  ],
  GESTOR: [
    { label: 'Dashboard', href: '/admin/dashboard' },
    { label: 'Gestión de Pedidos', href: '/admin/pedidos' },
  ],
  ADMIN: [
    { label: 'Dashboard', href: '/admin/dashboard' },
    { label: 'Pedidos', href: '/admin/pedidos' },
    { label: 'Productos', href: '/admin/productos' },
    { label: 'Categorías', href: '/admin/categorias' },
    { label: 'Stock', href: '/admin/stock' },
    { label: 'Usuarios', href: '/admin/usuarios' },
    { label: 'Sucursales', href: '/admin/sucursales' },
    { label: 'Puntos de Retiro', href: '/puntos-retiro' },
  ],
}

export function Navigation() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const cartItems = useCartStore((state) => state.items)
  const toggleCart = useUIStore((state) => state.toggleCart)

  const handleLogout = () => {
    logout()
  }

  // Obtener el primer rol del usuario para el menú
  const userRole = user?.roles?.[0] as keyof typeof MENU_BY_ROLE | undefined
  const menuItems = userRole ? MENU_BY_ROLE[userRole] || [] : []

  const totalCartItems = cartItems.reduce((sum, item) => sum + item.cantidad, 0)

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center">
              <Link to="/" className="text-xl font-bold text-indigo-600">
                Food Store
              </Link>
            </div>

            {/* Menu items */}
            {isAuthenticated && menuItems.length > 0 && (
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {menuItems.map((item) => (
                  <Link
                    key={item.href}
                    to={item.href}
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-700 hover:text-indigo-600"
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <button onClick={toggleCart} className="relative p-2 text-gray-600 hover:text-indigo-600 rounded-full hover:bg-gray-100 transition-colors" title="Ver carrito">
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
              </svg>
              {totalCartItems > 0 && (
                <span className="absolute -top-0.5 -right-0.5 bg-indigo-600 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {totalCartItems > 99 ? '99+' : totalCartItems}
                </span>
              )}
            </button>
            {!isAuthenticated ? (
              <div className="flex space-x-4">
                <Link
                  to="/login"
                  className="text-sm font-medium text-gray-700 hover:text-indigo-600"
                >
                  Ingresar
                </Link>
                <Link
                  to="/register"
                  className="text-sm font-medium text-white bg-indigo-600 px-4 py-2 rounded hover:bg-indigo-700"
                >
                  Registrarse
                </Link>
              </div>
            ) : (
              <div className="relative ml-3">
                <div className="flex items-center space-x-3">
                  <span className="text-sm font-medium text-gray-700">
                    {user?.nombre}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    Cerrar sesión
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
