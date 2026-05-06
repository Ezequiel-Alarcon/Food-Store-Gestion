# cart-store

Zustand store para gestión del carrito de compras.

## Estado Inicial

```typescript
interface CartItem {
  productoId: number;
  producto: {
    id: number;
    nombre: string;
    precio: number;
    imagenUrl: string;
  };
  cantidad: number;
  personalizacion: number[]; // IDs de ingredientes a excluir
}

interface CartState {
  items: CartItem[];
}
```

## Acciones Requeridas

- `addItem(producto, cantidad, personalizacion?)`: Agregar producto al carrito. Si ya existe, incrementa cantidad
- `removeItem(productoId)`: Elimin ar producto del carrito
- `updateQuantity(productoId, cantidad)`: Cambiar cantidad
- `clearCart()`: Vaciar carrito

## Selectores Requeridos

- `totalItems()`: Cantidad total de items
- `totalPrice()`: Suma de precio × cantidad
- `getItem(productoId)`: Obtener un item específico

## Persistencia

**Middleware:** Zustand persist
**Storage key:** `food-store-cart`
**Partialize:** Todo el objeto `items` se persiste

## Reglas de Negocio (RN-CR)

- RN-CR01: El carrito es client-side only (no existe en backend)
- RN-CR02: Persiste al cerrar navegador, refresh, y logout/login
- RN-CR03: Si el producto ya está, incrementar cantidad (no duplicar)
- RN-CR04: Solo excluir ingredientes que el producto tiene
- RN-CR05: Personalización es array de IDs de ingredientes

## Criterios de Éxito

- [ ] addItem() funciona con productos nuevos
- [ ] addItem() incrementa si el producto ya existe
- [ ] removeItem() elimina correctamente
- [ ] totalItems() retorna número correcto
- [ ] totalPrice() calcula correctamente
- [ ] Persiste en localStorage
- [ ] Recargar página reconstructiona el carrito