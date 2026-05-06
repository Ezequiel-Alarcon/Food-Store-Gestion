# design.md -- frontend-config

## Context

El proyecto Food Store necesita un frontend configurado para comenzar a implementar features. El change 1 (`infra-setup`) ya creó la estructura de carpetas FSD, pero falta configurar las herramientas, stores de estado y networking. El backend ya está configurado (change 2), pero el frontend aún no tiene las dependencias instaladas ni la configuración base.

## Goals / Non-Goals

**Goals:**
- Establecer el entorno de desarrollo con React + Vite funcionando
- Configurar Zustand para los 4 stores requeridos por la especificación
- Configurar Axios con interceptor JWT
- Configurar TanStack Query con provider
- Tener el proyecto compileando y corriendo en localhost:5173

**Non-Goals:**
- Implementar UI (componentes, páginas)
- Implementar features de autenticación
- Integrar con el backend (eso viene en siguientes changes)

## Decisions

### D1: Estructura de stores

**Decision:** Un archivo por store, no un archivo monolítico.

**Rationale:** La especificación (v5.0, sección 9) requiere 4 stores separados con responsabilidades claras:
- `authStore`: tokens JWT, usuario, isAuthenticated. Persiste solo accessToken
- `cartStore`: items del carrito. Persiste items completos
- `paymentStore`: estado del proceso de pago. NO persiste
- `uiStore`: estado UI local (modales, sidebar). NO persiste (excepto theme)

Separar en archivos permite:
- Importación selectiva (no cargar todo)
- Mantenimiento más fácil
- Testing individual

**Alternatives considered:**
- Un solo store con slices: viola la separación de responsabilidades de la spec
- Libraries externas (Redux, Recoil): no están en el stack definido

### D2: Persistencia del authStore

**Decision:** Usar middleware persist de Zustand con partialize, PersistState de localStorage.

**Rationale:** La spec dice: "persiste solo accessToken". El problema es que Zustand persist guarda el state completo. La solución es usar `partialize` para especificar qué campos se persistir.

```typescript
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // ... actions
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({ accessToken: state.accessToken }),
    }
  )
)
```

**Alternatives considered:**
- Guardar todo en localStorage: inseguro (exponer refresh token)
- No guardar nada: forzar re-login en cada refresh → mala UX

### D3: Interceptor de Axios

**Decision:** Interceptor de request para JWT + interceptor de response para 401 → refresh → retry.

**Rationale:** La spec requiere:
- Agregar Authorization: Bearer <token> a cada request
- Manejar 401 automáticamente (RN-AU02, access token 30 min)
- Refresh transparente (RN-AU04)

**Alternatives considered:**
- Fetch API: menor soporte de interceptors, más boilerplate
- React Query prefetch: no maneja auth header automáticamente

### D4: TanStack Query configuration

**Decision:** QueryClient con defaults razonables, QueryClientProvider envuelto en App.

**Rationale:**
- `staleTime`: 5 minutos (evitar refetch constante)
- `retry`: 1 (no infinite loop en errores)
- `refetchOnWindowFocus`: false (evitar refetch molesto)

**Alternatives considered:**
- Defaults de cero: demasiado refetching
- Configuración por query: overkill para setup inicial

### D5: TypeScript strict

**Decision:** strict:true en tsconfig.json, sin any.

**Rationale:** La spec dice "strict: true, no any". Esto fuerza tipado correcto y previene errores en runtime.

**Alternatives considered:**
- loose TypeScript: técnico pero genera deuda

## Risks / Trade-offs

### R1: MercaderPago SDK en frontend

**Risk:** El SDK oficial (@mercadopago/sdk-js) puede tener limitaciones en entorno de desarrollo.

**Mitigation:** Usar el SDK siempre, pero tener la public key de test en .env.example. Si falla, el checkout redirecciona a MP (solución de fallback).

### R2: Persistencia del cartStore

**Risk:** Si un producto se modifica o elimina en backend, el cart local queda desincronizado.

**Mitigation:** En el siguiente change (`products-module`), agregar validación al crear pedido que verifique disponibilidad y precio actual.

### R3: Dual store (Zustand + TanStack Query)

**Risk:** Confusión sobre qué estado vive en cada uno.

**Mitigation:** Respetar la regla de la spec: Zustand = estado CLIENTE (local), TanStack Query = estado SERVIDOR (remoto). No mezclarlos.

## Migration Plan

1. Crear `/frontend/package.json` con todas las dependencias
2. Crear `/frontend/vite.config.ts`
3. Crear `/frontend/tsconfig.json` con strict:true
4. Crear `/frontend/tailwind.config.js` y postcss.config.js
5. Instalar dependencias: `npm install`
6. Verificar `npm run dev` levanta en 5173
7. Crear stores en `/frontend/src/stores/`
8. Crear API en `/frontend/src/lib/api.ts`
9. Configurar providers en `/frontend/src/App.tsx`

## Open Questions

- **Q1:** ¿Usar el SDK de MercadoPago para React (@mercadopago/sdk-react) o el vanilla (@mercadopago/sdk-js)? 
  - **Respuesta предполагает:** El vanilla es más flexible, maar el SDK de React streamlinea el Card Payment. Usar vanilla para máximo control.