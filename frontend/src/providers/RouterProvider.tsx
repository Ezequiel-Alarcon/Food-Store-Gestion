import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ReactNode } from 'react'
import { LoginForm } from '../features/auth/LoginForm'
import { RegisterForm } from '../features/auth/RegisterForm'
import { ProtectedRoute } from '../features/auth/ProtectedRoute'
import { Navigation } from '../features/layout/Navigation'
import { MisDireccionesPage } from '../features/addresses/MisDireccionesPage'
import { PickupPointsPage } from '../features/addresses/PickupPointsPage'
import { CatalogPage } from '../pages/CatalogPage'
import { CartPage } from '../pages/CartPage'
import { CartDrawer } from '../features/cart/CartDrawer'
import { ConfirmModal } from '../features/layout/ConfirmModal'
import { ToastContainer } from '../features/layout/ToastContainer'
import { OrdersPage } from '../features/orders'
import { ProfilePage } from '../pages/ProfilePage'
import CheckoutPage from '../pages/CheckoutPage'
import { OrdersListPage } from '../features/admin/orders/ui/OrdersListPage'
import { OrderDetailPage } from '../features/admin/orders/ui/OrderDetailPage'
import { UsersPage } from '../features/admin/users/ui/UsersPage'
import { DashboardPage } from '../features/admin/dashboard'
import { StockManagementPage } from '../features/admin/stock'
import { CategoriesPage } from '../features/admin/categories'
import { ProductsPage } from '../features/admin/products'

interface RouterProviderProps {
  children: ReactNode
}

export function RouterProvider({ children }: RouterProviderProps) {
  return (
    <BrowserRouter>
      <Navigation />
      <CartDrawer /><ConfirmModal /><ToastContainer />
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={children} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        <Route path="/productos" element={<CatalogPage />} />
        <Route path="/carrito" element={<CartPage />} />

        {/* Rutas protegidas - Cliente */}
        <Route
          path="/pedidos"
          element={
            <ProtectedRoute allowedRoles={['CLIENT']}>
              <OrdersPage />
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

        <Route
          path="/checkout"
          element={
            <ProtectedRoute allowedRoles={['CLIENT']}>
              <CheckoutPage />
            </ProtectedRoute>
          }
        />

        {/* Rutas protegidas - Admin */}
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedRoute allowedRoles={['ADMIN', 'GESTOR']}>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={['ADMIN', 'PEDIDOS', 'STOCK']}>
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
              <UsersPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/stock"
          element={
            <ProtectedRoute allowedRoles={['STOCK', 'ADMIN']}>
              <StockManagementPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/categorias"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <CategoriesPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/productos"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <ProductsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/pedidos/:id"
          element={
            <ProtectedRoute allowedRoles={['PEDIDOS', 'ADMIN']}>
              <OrderDetailPage />
            </ProtectedRoute>
          }
        />

        {/* Perfil */}
        <Route
          path="/perfil"
          element={
            <ProtectedRoute allowedRoles={['CLIENT', 'ADMIN', 'STOCK', 'PEDIDOS', 'GESTOR']}>
              <ProfilePage />
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
