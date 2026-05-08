import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ReactNode } from 'react'
import { LoginForm } from '../features/auth/LoginForm'
import { RegisterForm } from '../features/auth/RegisterForm'
import { ProtectedRoute } from '../features/auth/ProtectedRoute'
import { Navigation } from '../features/layout/Navigation'
import { MisDireccionesPage } from '../features/addresses/MisDireccionesPage'
import { PickupPointsPage } from '../features/addresses/PickupPointsPage'

interface RouterProviderProps {
  children: ReactNode
}

export function RouterProvider({ children }: RouterProviderProps) {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={children} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        {/* Rutas protegidas - Cliente */}
        <Route
          path="/pedidos"
          element={
            <ProtectedRoute allowedRoles={['CLIENT']}>
              <div className="p-8">
                <h1 className="text-2xl font-bold">Mis Pedidos</h1>
                <p className="text-gray-600 mt-2">Aquí verás tus pedidos</p>
              </div>
            </ProtectedRoute>
          }
        />

        <Route
          path="/direcciones"
          element={
            <ProtectedRoute allowedRoles={['CLIENT']}>
              <MisDireccionesPage />
            </ProtectedRoute>
          }
        />

        <Route path="/puntos-retiro" element={<PickupPointsPage />} />

        {/* Rutas protegidas - Admin */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={['ADMIN', 'GESTOR_PEDIDOS', 'GESTOR_STOCK']}>
              <div className="p-8">
                <h1 className="text-2xl font-bold">Dashboard</h1>
                <p className="text-gray-600 mt-2">Panel de administración</p>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/usuarios"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <div className="p-8">
                <h1 className="text-2xl font-bold">Gestión de Usuarios</h1>
                <p className="text-gray-600 mt-2">Administración de usuarios</p>
              </div>
            </ProtectedRoute>
          }
        />

        {/* Redirección por defecto */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export { BrowserRouter, Routes, Route, Navigate }
