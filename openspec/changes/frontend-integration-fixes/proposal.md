## Why

Dos bugs funcionales fueron identificados durante code review del frontend. El primero es crítico: `App.tsx` no renderiza los children que le pasa `RouterProvider`, lo que significa que las rutas definidas en `RouterProvider` nunca se alcanzan cuando `/` está activa. El segundo es un edge case del flujo de pago donde el estado `'redirecting'` queda huérfano si el usuario cierra el navegador durante el redirect a MercadoPago.

## What Changes

- **BUG-1 Fix**: Modificar `App.tsx` para que renderice `children` (delegando al router en lugar de HTML hardcodeado)
- **BUG-2 Fix**: Agregar timeout o fallback en `paymentStore` para el estado `'redirecting'` para manejar el caso donde el usuario no vuelve de MercadoPago

## Capabilities

### New Capabilities

- _(Ninguna — son fixes de bugs existentes)_

### Modified Capabilities

- `checkout-frontend`: El estado de checkout ahora maneja correctamente el timeout del redirect a MercadoPago

## Impact

**Frontend:**
- `frontend/src/App.tsx` — hacer que renderice `children` prop
- `frontend/src/stores/paymentStore.ts` — agregar timeout o reset para el estado `'redirecting'`