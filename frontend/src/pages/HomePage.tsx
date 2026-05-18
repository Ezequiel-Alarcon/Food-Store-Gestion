import { Link } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'

export function HomePage() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const user = useAuthStore((s) => s.user)

  if (isAuthenticated && user) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900">¡Hola, {user.nombre}!</h1>
          <p className="text-gray-600 mt-2 text-lg">¿Qué vas a pedir hoy?</p>
          <div className="flex gap-4 mt-6">
            <Link
              to="/productos"
              className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
            >
              Ver Catálogo
            </Link>
            <Link
              to="/pedidos"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Mis Pedidos
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-indigo-600 to-indigo-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
            🍔 Food Store
          </h1>
          <p className="mt-4 text-xl text-indigo-100 max-w-2xl mx-auto">
            Tu comida favorita, a un click de distancia. Pedí online, rápido y fácil.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/login"
              className="inline-flex items-center justify-center px-8 py-3 bg-white text-indigo-700 rounded-lg font-semibold hover:bg-indigo-50 transition-colors shadow-lg"
            >
              Ingresar
            </Link>
            <Link
              to="/register"
              className="inline-flex items-center justify-center px-8 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white/10 transition-colors"
            >
              Registrarse
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🛒</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Pedí online</h3>
            <p className="text-gray-500">Explorá nuestro catálogo y armá tu pedido en minutos. Sin llamadas, sin esperas.</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🚀</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Rápido y fácil</h3>
            <p className="text-gray-500">Pagá con MercadoPago en segundos. Tarjeta, Rapipago o Pago Fácil.</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📦</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Seguí tu orden</h3>
            <p className="text-gray-500">Rastreá tu pedido en tiempo real. Desde la cocina hasta tu puerta.</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">¿Listo para pedir?</h2>
          <p className="text-gray-600 mb-8">Creá tu cuenta gratis y empezá a disfrutar.</p>
          <Link
            to="/register"
            className="inline-flex items-center px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors shadow-lg"
          >
            Crear Cuenta Gratis
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-sm text-gray-500">
          Food Store © 2026 · Todos los derechos reservados
        </div>
      </footer>
    </div>
  )
}
