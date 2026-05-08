import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

// Definición de menú por rol
const MENU_BY_ROLE: Record<string, Array<{ label: string; href: string }>> = {
  CLIENT: [
    { label: 'Productos', href: '/productos' },
    { label: 'Mis Pedidos', href: '/pedidos' },
  ],
  GESTOR_STOCK: [
    { label: 'Productos', href: '/productos' },
    { label: 'Gestión de Stock', href: '/admin/stock' },
  ],
  GESTOR_PEDIDOS: [
    { label: 'Productos', href: '/productos' },
    { label: 'Gestión de Pedidos', href: '/admin/pedidos' },
  ],
  ADMIN: [
    { label: 'Dashboard', href: '/admin' },
    { label: 'Gestión de Usuarios', href: '/admin/usuarios' },
  ],
}

export function Navigation() {
  const navigate = useNavigate()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  // Obtener el primer rol del usuario para el menú
  const userRole = user?.roles?.[0] as keyof typeof MENU_BY_ROLE | undefined
  const menuItems = userRole ? MENU_BY_ROLE[userRole] || [] : []

  return (
    <nav className="bg-white shadow">
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
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-indigo-600"
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Right side */}
          <div className="flex items-center">
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