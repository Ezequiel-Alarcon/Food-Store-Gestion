# payment-store

Zustand store para gestión del proceso de pago con MercadoPago.

## Estado Inicial

```typescript
interface PaymentState {
  checkoutStep: 'idle' | 'creating' | 'redirecting' | 'processing' | 'approved' | 'rejected' | 'error';
  preferenceId: string | null;
  paymentStatus: 'pending' | 'approved' | 'rejected' | 'error' | null;
  statusDetail: string | null;
  error: string | null;
}
```

## Acciones Requeridas

- `startCheckout(pedidoId)`: Iniciar proceso (checkoutStep = 'creating')
- `setPreference(preferenceId)`: Preferencia creada (checkoutStep = 'redirecting')
- `updatePaymentStatus(status, statusDetail?)`: Actualizar estado del pago
- `resetPayment()`: Reset a estado inicial

## Persistencia

**NO persiste.** Reset al recargar la página.

> **Rationale:** El proceso de pago es transitorio. Si el usuario recarga, debe empezar de nuevo.

## Criterios de Éxito

- [ ] startCheckout() setea el step correcto
- [ ] resetPayment() limpia todo
- [ ] No persiste en localStorage
- [ ] Recargar página limpia el estado