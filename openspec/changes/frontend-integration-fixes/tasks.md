## 1. App.tsx Fix

- [ ] 1.1 Modificar `App.tsx` para recibir `children` prop
- [ ] 1.2 Reemplazar el HTML hardcodeado por `return children ?? null`
- [ ] 1.3 Importar `React` si es necesario

## 2. PaymentStore Timeout

- [ ] 2.1 Agregar timeout de 30s en `setPreference` que llame `updatePaymentStatus('cancelled', 'timeout')`
- [ ] 2.2 Verificar que el timeout no interfiera con retornos normales de MP

## 3. Verification

- [ ] 3.1 Verificar TypeScript compilation — `pnpm exec tsc --noEmit`
- [ ] 3.2 Commit con conventional commits