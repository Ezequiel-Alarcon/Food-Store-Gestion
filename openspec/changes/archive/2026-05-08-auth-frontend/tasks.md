# tasks.md -- auth-frontend

## 1. Extender authStore con API

- [ ] 1.1 Extender authStore con método login que llama a POST /api/v1/auth/login
- [ ] 1.2 Extender authStore con método register que llama a POST /api/v1/auth/register
- [ ] 1.3 Extender authStore con método refreshToken que llama a POST /api/v1/auth/refresh
- [ ] 1.4 Agregar método logout en authStore que limpie tokens, usuario, y rediriga

## 2. Actualizar API con interceptor 401

- [ ] 2.1 Modificar api.ts para agregar interceptor de response que captura 401
- [ ] 2.2 Implementar lógica de retry con refresh token (guardar request original, fazer refresh, reintentar)
- [ ] 2.3 Agregar mutex flag para evitar múltiples refresh simultáneos
- [ ] 2.4 Manejar refresh fallido (logout + redirect a /login)

## 3. LoginForm Component

- [ ] 3.1 Crear archivo frontend/src/features/auth/LoginForm.tsx
- [ ] 3.2 Implementar formulario con TanStack Form (email, password inputs)
- [ ] 3.3 Agregar validación: email requerido y formato válido
- [ ] 3.4 Agregar validación: password requerido
- [ ] 3.5 Conectar con authStore.login en submit
- [ ] 3.6 Agregar estado de loading (botón disabled, texto "Cargando...")
- [ ] 3.7 Agregar link a /register

## 4. RegisterForm Component

- [ ] 4.1 Crear archivo frontend/src/features/auth/RegisterForm.tsx
- [ ] 4.2 Implementar formulario con TanStack Form (nombre, email, password, confirmarPassword)
- [ ] 4.3 Agregar validación: nombre requerido
- [ ] 4.4 Agregar validación: email requerido y formato válido
- [ ] 4.5 Agregar validación: password mínimo 8 caracteres
- [ ] 4.6 Agregar validación: password debe coincidir con confirmarPassword
- [ ] 4.7 Conectar con authStore.register en submit
- [ ] 4.8 Agregar estado de loading
- [ ] 4.9 Agregar link a /login

## 5. ProtectedRoute Component

- [ ] 5.1 Crear archivo frontend/src/features/auth/ProtectedRoute.tsx
- [ ] 5.2 Componente que recibe prop roles (array de strings, opcional)
- [ ] 5.3 Verificar isAuthenticated del store, redirigir a /login si no
- [ ] 5.4 Verificar roles si se proveen, redirigir a home si no tiene
- [ ] 5.5 Preservar returnUrl en query param

## 6. Navigation Component

- [ ] 6.1 Crear archivo frontend/src/features/layout/Navigation.tsx
- [ ] 6.2 Mostrar "Ingresar" y "Registrarse" si no autenticado
- [ ] 6.3 Mostrar dropdown con nombre de usuario si autenticado
- [ ] 6.4 Filtrar opciones de menú por rol del usuario
- [ ] 6.5 Implementar logout que llame authStore.logout() y redirija

## 7. Toast / Error Handling

- [ ] 7.1 Verificar que hay ToastProvider en App.tsx (del frontend-config)
- [ ] 7.2 Mostrar toast en error de login (credenciales inválidas)
- [ ] 7.3 Mostrar toast en error de registro (email existe)
- [ ] 7.4 Mostrar toast en sesión expirada (refresh falló)
- [ ] 7.5 Mostrar toast en acceso no autorizado

## 8. Rutas de Auth

- [ ] 8.1 Crear LoginPage que renderiza LoginForm
- [ ] 8.2 Crear RegisterPage que renderiza RegisterForm
- [ ] 8.3 Agregar rutas /login y /register en el router
- [ ] 8.4 Proteger rutas /perfil, /pedidos, /admin/* con ProtectedRoute

## 9. Verificación

- [ ] 9.1 npm run build sin errores
- [ ] 9.2 Verificar login con credenciales válidas guarda token y redirige
- [ ] 9.3 Verificar login con credenciales inválidas muestra error
- [ ] 9.4 Verificar registro funciona y redirige a home
- [ ] 9.5 Verificar ProtectedRoute redirige a login si no autenticado
- [ ] 9.6 Verificar Navigation muestra menú correcto por rol
- [ ] 9.7 Verificar logout limpia sesión y muestra opciones de guest