## Context

El `auth-backend` (change #6) ya está implementado y archivado, proporcionando los endpoints:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout
- GET /api/v1/perfil
- PUT /api/v1/perfil
- PUT /api/v1/perfil/password

El `frontend-config` (change #3) está implementado y archivado, proporcionando:
- authStore con persistencia de accessToken
- api.ts con interceptor de request (Authorization header)
- stores de Zustand: authStore, cartStore, paymentStore, uiStore

El problema actual: no hay UI para autenticarse, no hay protección de rutas por rol, y el interceptor 401 parcial maneja refresh pero falta retry de la request original.

## Goals / Non-Goals

**Goals:**
- LoginForm y RegisterForm funcionales con validación de inputs y estados de loading/error
- ProtectedRoute que verifica accessToken y rol del usuario
- Navigation dinâmica que muestra opciones de menú según rol (CLIENT, GESTOR_STOCK, GESTOR_PEDIDOS, ADMIN)
- Retry automático de request tras refresh de token (no simplemente redirigir a login)
- Manejo centralizado de errores de auth con toast notifications

**Non-Goals:**
- Implementación de página de perfil (se hace en change futuro si aplica)
- Implementación de olvidé mi contraseña (fuera del scope)
- Tests automatizados (se agregan después)
- Dashboard de admin (cambios #16-18)

## Decisions

### D1: Componentes de formulario

**Decisión**: Usar TanStack Form para validación de inputs en lugar de react-hook-form o formik.

**Alternativas consideradas**:
- react-hook-form: más popular pero mayor bundle size
- formik: más simple pero sin integración con TanStack Query

**Rationale**: Ya tenemos TanStack Query instalado (del frontend-config), usar TanStack Form mantiene consistencia en el stack y reduce dependencias. La API es similar a react-hook-form pero más liviana.

**D2: Estructura del authStore

Decisión: Extender el authStore existente con actions que llaman a la API en lugar de crear uno nuevo.

Rationale: El frontend-config ya creó un authStore básico con login/logout/updateTokens. Extenderlo mantiene consistencia y reduce código duplicado.

### D3: ProtectedRoute con role checking

Decisión: Componente que recibe array de roles permitidos y verifica contra authStore.user.rol.

Alternativas consideradas:
- Solo verificar autenticación (boolean)
- Verificar rol en cada page component

Rationale: El sistema requiere RBAC completo (ADMIN, GESTOR_STOCK, GESTOR_PEDIDOS, CLIENT). Proteger a nivel de ruta es más seguro que verificar en cada componente.

### D4: Retry de request tras refresh

Decisión: El interceptor 401 guarda la request original, intenta refresh, y re-ejecuta la request original.

Rationale: El flujo actual simplemente rechaza con 401. El usuario debe reintentarla manualmente. Mejor UX es reintentarla automáticamente.

### D5: Navegación por rol

Decisión: Navigation lee authStore.user.rol y filtra las opciones de menú visibles.

Rationale:Cada rol tiene diferentes funcionalidades. CLIENT ve pedidos propios, ADMIN ve dashboard y gestión de usuarios, etc.

## Risks / Trade-offs

[Riesgo 1]: Refresh token expira durante una request
→ Mitigación: Si refresh falla (token vencido o inválido), hacer logout y redirigir a login

[Riesgo 2]: Race condition entre múltiples requests con 401 simultáneo
→ Mitigación: Usar un flag mutex para evitar múltiples refresh simultáneos

[Riesgo 3]: authStore no tiene el role del usuario después de login
→ Mitigación: El endpoint /auth/login retorna el usuario completo con rol. Guardar en store.

[Riesgo 4]: Menú no muestra las opciones correctas según rol
→ Mitigación: Verificar que el role se persiste correctamente desde el backend

## Open Questions

- ¿Se usa un componente de Navigation existente o se crea desde cero?
- ¿El logout debe limpiar el carrito también? (probable que sí, pero confirmar)
- ¿Manejo de errores va en un ToastProvider global o en cada componente?