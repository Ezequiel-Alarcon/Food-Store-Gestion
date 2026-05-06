import { useAuthStore } from './stores/authStore'

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return (
    <div className="min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold text-gray-900 p-8">
        Food Store -Bienvenido
      </h1>
      <p className="px-8 text-gray-600">
        {isAuthenticated ? 'Estas logueado' : 'Inicia sesion para ordenar'}
      </p>
    </div>
  )
}

export default App