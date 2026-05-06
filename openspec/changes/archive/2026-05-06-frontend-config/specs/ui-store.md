# ui-store

Zustand store para estado de UI local del cliente.

## Estado Inicial

```typescript
interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  cartOpen: boolean;
  confirmModal: {
    open: boolean;
    title: string;
    message: string;
    onConfirm: (() => void) | null;
  };
  toasts: Array<{
    id: string;
    type: 'success' | 'error' | 'info' | 'warning';
    message: string;
  }>;
}
```

## Acciones Requeridas

- `setTheme(theme)`: Cambiar tema
- `toggleSidebar()`: Toggle sidebar
- `openCart()`: Abrir carrito
- `closeCart()`: Cerrar carrito
- `toggleCart()`: Toggle carrito
- `openConfirmModal(title, message, onConfirm)`: Abrir modal de confirmación
- `closeConfirmModal()`: Cerrar modal
- `addToast(type, message)`: Agregar toast
- `removeToast(id)`: Remover toast

## Persistencia

**Middleware:** Zustand persist
**Storage key:** `food-store-ui`
**Partialize:** Solo `theme` se persiste

> **Rationale:**Solo el tema persiste. El resto es estado transitorio de sesión.

## Criterios de Éxito

- [ ] Theme se persiste en localStorage
- [ ] Sidebar/cart no persisten
- [ ] toasts se pueden agregar/remover
- [ ] Recargar página reconstructiona solo el theme