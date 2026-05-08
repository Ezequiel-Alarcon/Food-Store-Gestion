import { useAuthStore } from './stores/authStore'

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return (
    <>
      <div className="min-h-screen bg-gray-50">
        {isAuthenticated ? (
          <div className="py-8 px-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Food Store - Bienvenido
            </h1>
            <p className="mt-2 text-gray-600">
              ¡Bienvenido de nuevo!
            </p>
          </div>
        ) : (
          <div className="py-8 px-4">
            <h1 className="text-3xl font-bold text-gray-900 text-center">
              Food Store
            </h1>
            <p className="mt-2 text-gray-600 text-center">
              Iniciá sesión para ordenar
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <a
                href="/login"
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700"
              >
                Ingresar
              </a>
              <a
                href="/register"
                className="px-6 py-3 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300"
              >
                Registrarse
              </a>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

export default App
