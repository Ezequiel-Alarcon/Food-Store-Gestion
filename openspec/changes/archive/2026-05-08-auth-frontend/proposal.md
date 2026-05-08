## Why

El backend de autenticación ya está implementado (auth-backend change #6), pero el frontend carece de la interfaz de login/register, navegación protegida y manejo de tokens. Sin auth-frontend, el usuario no puede autenticarse en la aplicación, no hay protección de rutas, y el refresh automático de tokens no funciona. Este change habilita la experiencia de usuario para authenticate en la app.

## What Changes

- **LoginForm y RegisterForm**: Componentes de React en `features/auth/` con validación de inputs, errores RFC 7807, y estados de loading
- **ProtectedRoute**: Componente de ruta protegida que redirige a login si no hay accessToken
- **Auth Guards**: Lógica por rol (CLIENT, GESTOR_STOCK, GESTOR_PEDIDOS, ADMIN)
- **Navigation**: Menú dinámico según rol del usuario desde authStore
- **Interceptor 401**: Retry automático con refresh token antes de rechazar la request
- **Manejo de errores globales**: Notificaciones toast para errores de autenticación

## Capabilities

### New Capabilities

- `login-form`: Formulario de login con email/password, validación, submit al endpoint /auth/login
- `register-form`: Formulario de registro con nombre/email/password, validación, submit al endpoint /auth/register
- `protected-route`: Componente Routewrapper que protege rutas según autenticación y rol
- `auth-navigation`: Navegación dinâmica que muestra menú según rol del usuario
- `auto-token-refresh`: Interceptor Axios que maneja 401 y renueva accessToken automáticamente
- `auth-error-handler`: Manejo centralizado de errores de autenticación con toast notifications

### Modified Capabilities

- `auth-store`: Se amplía con métodos de login/register/refresh y persistencia de user con role

## Impact

- **`frontend/src/features/auth/`**: LoginForm.tsx, RegisterForm.tsx, AuthProvider.tsx
- **`frontend/src/features/layout/`**: ProtectedRoute.tsx, Navigation.tsx
- **`frontend/src/middleware/`**: authInterceptor.ts (401 handler)
- **`frontend/src/stores/`**: authStore se extiende con actions de API
- **`frontend/src/lib/api.ts`**: Se agrega interceptor de response para 401
- **Dependencies**: `auth-backend` (✅ archivado), `frontend-config` (✅ archivado)