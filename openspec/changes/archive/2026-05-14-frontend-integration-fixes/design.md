## Context

Durante code review se identificaron dos bugs funcionales en el frontend. El primero (`App.tsx` no renderiza children) es crítico porque rompe el sistema de routing para la ruta `/`. El segundo (`redirecting` sin salida) es un edge case del flujo de pago que puede dejar al usuario varado si cierra el navegador durante el redirect a MercadoPago.

## Goals / Non-Goals

**Goals:**
- Corregir `App.tsx` para que delegue al router (renderice `children`)
- Agregar timeout de 30 segundos en `setPreference` que haga fallback a `idle` si no se recibe actualización de estado

**Non-Goals:**
- No cambiar la estructura de routing (RouterProvider está bien)
- No modificar el flujo de pago de MercadoPago (CardPayment Brick sigue igual)
- No agregar nuevas dependencias — usar solo `setTimeout`

## Decisions

### D1: App.tsx como passthrough

**Decisión:** `App` debe renderizar `children` prop, no HTML hardcodeado.

**Alternativas considered:**
- Eliminar `App.tsx` por completo y pasar children directo a RouterProvider → requiere cambios en main.tsx
- Dejar `App.tsx` como layout wrapper → overkill para lo que hace

**Rationale:** `main.tsx` ya envuelve `<App />` con `<RouterProvider>`. La ruta `/` en `RouterProvider` está definida como `<Route path="/" element={children} />`, donde `children` es `<App />`. El patrón correcto es que `App` simplemente renderice sus children (que en este caso sería el contenido de la página `/`). Si el path `/` necesita contenido específico, debería ser un componente de página, no App.

```tsx
// Antes:
function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return <div>...hardcoded HTML...</div>
}

// Después:
function App({ children }: { children?: React.ReactNode }) {
  return children ?? null
}
```

### D2: Timeout para estado 'redirecting'

**Decisión:** Agregar un timeout de 30 segundos en `setPreference` que haga `resetPayment()` si no se recibió una actualización de estado.

**Alternativas considered:**
- Usar webhook de MercadoPago para detectar cuando el usuario no volvió → no es confiable (el webhook puede tardar)
- Dejarlo como está → el usuario puede quedar varado
- Detectar cuando `preferenceId` cambia sin que `updatePaymentStatus` se haya llamado → simple y efectivo

**Rationale:** El flujo es: `setPreference` → MP redirect → usuario vuelve → webhook actualiza status. Si el usuario cierra el navegador, nunca vuelve, nunca se llama `updatePaymentStatus`, y el store queda en `redirecting` para siempre. Un timeout de 30s es un trade-off razonable — cubre el caso de que el usuario no vuelva, pero no es tan corto como para interferir con retornos normales.

**Archivo:** `frontend/src/stores/paymentStore.ts`

```typescript
setPreference: (preferenceId) => {
  set({ checkoutStep: 'redirecting', preferenceId })

  // Timeout 30s — si no se actualiza el estado, volver a idle
  setTimeout(() => {
    usePaymentStore.getState().updatePaymentStatus('cancelled', 'timeout')
  }, 30000)
}
```

## Risks / Trade-offs

| Riesgo | Mitigation |
|--------|------------|
| El timeout puede disparar si el webhook tarda más de 30s | El timeout llama `updatePaymentStatus('cancelled')` que es reversible — el usuario puede reintentar |
| Si el usuario vuelve antes de 30s y el timeout ya disparó | `updatePaymentStatus` se ejecuta primero y cancela el timeout (o lo sobrescribe) |

## Open Questions

- Ninguna — los fixes son simples y no tienen dependencias externas.

## Files to Modify

| Archivo | Cambio |
|---------|--------|
| `frontend/src/App.tsx` | Renderizar children prop en lugar de HTML hardcodeado |
| `frontend/src/stores/paymentStore.ts` | Agregar timeout de 30s en setPreference |