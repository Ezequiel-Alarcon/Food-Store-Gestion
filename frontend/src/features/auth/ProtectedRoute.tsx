import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore, type User } from '../../stores/authStore'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles?: User['roles']
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const location = useLocation()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const user = useAuthStore((state) => state.user)

  // Si no está autenticado, redirigir a login preservando returnUrl
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  // Si hay restricciones de rol, verificar
  if (allowedRoles && allowedRoles.length > 0) {
    const userRoles = user?.roles || []
    const hasRole = allowedRoles.some((role) => userRoles.includes(role))

    if (!hasRole) {
      return <Navigate to="/" replace />
    }
  }

  return <>{children}</>
}