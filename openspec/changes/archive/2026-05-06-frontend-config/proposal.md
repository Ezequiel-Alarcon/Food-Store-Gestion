# proposal.md -- frontend-config

## Why

El frontend requiere estar configurado con React, Vite, Zustand y TanStack Query antes de implementar cualquier feature. Sin esta configuración, no hay entorno de desarrollo ni stores de estado para el resto del proyecto. Este change es blocking para `auth-frontend` y todos los features que dependan del estado del cliente.

## What Changes

- Setup completo de React 18+ con Vite 5+
- Tailwind CSS 3.x configurado con PostCSS
- TypeScript strict:true, sin any
- 4 Zustand stores: authStore, cartStore, paymentStore, uiStore
- Axios con interceptor JWT para Authorization header
- TanStack Query (QueryClient) configurado con provider
- React Router DOM con rutas base
- Interceptor de respuesta que maneja 401 y refresh automático
- Stores con persistencia en localStorage (excepto paymentStore)
- Variables de entorno con prefix VITE_

## Capabilities

### New Capabilities

- `frontend-setup`: Configuración base del proyecto frontend con todas las dependencias, tooling y stores de estado
- `auth-store`: Zustand store para autenticación con persistencia de accessToken
- `cart-store`: Zustand store para carrito de compras con persistencia
- `payment-store`: Zustand store para proceso de pago (sin persistencia)
- `ui-store`: Zustand store para estado de UI local

### Modified Capabilities

- Ninguna (es setup inicial)

## Impact

- **`frontend/`**: Toda la estructura base FSD se crea o actualiza
- **`frontend/src/stores/`**: 4 archivos de stores
- **`frontend/src/lib/api.ts`**: Axios instance con interceptores
- **`frontend/src/providers/`**: QueryClient provider, Router provider
- Dependencias npm: react, react-dom, react-router-dom, @tanstack/react-query, @tanstack/react-form, zustand, axios, recharts, tailwindcss, @mercadopago/sdk-js