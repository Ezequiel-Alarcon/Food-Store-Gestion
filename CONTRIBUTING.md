# Contributing to Food Store

## Overview

Food Store uses **Spec-Driven Development (SDD)** with OPSX. All work is organized into **changes**, each with three artifacts: proposal, design, and tasks.

## Golden Rules

1. **Always read the docs first**
   - `docs/Integrador.txt` — Technical specification
   - `docs/CHANGES-ROADMAP.md` — Your change
   - `docs/Historias_de_usuario.txt` — User stories

2. **No code without specs**
   - Proposal must be reviewed
   - Design must be approved
   - Only then implement

3. **Architectural Integrity**
   - Backend: Router → Service → UoW → Repository → Model
   - Frontend: Features don't import from features
   - No circular dependencies

4. **Atomic Changes**
   - One change = one feature or capability
   - Max 12 files modified per change
   - Max 6 user stories per change

## Architecture Principles

### Backend: Clean Architecture

```
HTTP Request
    ↓
Router (HTTP parsing, validation)
    ↓
Service (business logic)
    ↓
Unit of Work (transaction)
    ↓
Repository (data access)
    ↓
Model (database entity)
```

**Rules:**
- Each layer imports ONLY from layers below
- Router never contains business logic
- Service never calls database directly (use UoW)
- Models never import from services or routers

**Example (CORRECT):**
```python
# In auth/service.py
async def register_user(uow: UnitOfWork, email: str, password: str):
    # Service calls repository through UoW
    existing = await uow.usuarios.get_by_email(email)
    if existing:
        raise ValueError("User exists")
    # UoW handles commit/rollback
    async with uow:
        user = Usuario(email=email, password_hash=hash(password))
        uow.usuarios.add(user)
        await uow.commit()
    return user
```

### Frontend: Feature-Sliced Design (FSD)

```
app (providers, routing)
  ↓ (unidirectional imports)
pages (route components)
  ↓
features (user interactions)
  ↓
entities (domain models, API)
  ↓
shared (UI components, utilities)
```

**Rules:**
- Features NEVER import from other features
- Pages NEVER import from pages
- Shared NEVER imports from features

**Example (CORRECT):**
```typescript
// In features/auth/components/LoginForm.tsx
import { Button, Input } from '@/shared/ui'      // ✅ OK
import { useLogin } from '@/features/auth/hooks' // ✅ OK
import { User } from '@/entities/models'         // ✅ OK

// NOT these:
// import { CartDrawer } from '@/features/cart'  // ❌ NO
// import { HomePage } from '@/pages'            // ❌ NO
```

## Database Patterns

### Unit of Work (UoW)
Manages database transactions:

```python
async with UnitOfWork() as uow:
    user = await uow.usuarios.get(id=1)
    user.email = "new@example.com"
    # Commit happens automatically on context exit
```

### BaseRepository[T]
Generic repository for CRUD:

```python
class UsuarioRepository(BaseRepository[Usuario]):
    async def get_by_email(self, email: str):
        return await self.session.execute(
            select(Usuario).where(Usuario.email == email)
        )
```

### Snapshot Pattern
Capture prices/details at order time:

```python
# When creating order, snapshot product price
price_snapshot = producto.precio  # Capture current price
detalle = DetallePedido(
    producto_id=producto.id,
    cantidad=cantidad,
    precio_unitario_snapshot=price_snapshot  # Frozen for audit trail
)
```

### Append-Only Audit Trail
Order status history never updates, only appends:

```python
# ❌ WRONG - updates existing record
await uow.historial_estado.update(id=1, estado_a="ENTREGADO")

# ✅ CORRECT - inserts new record
historial = HistorialEstadoPedido(
    pedido_id=pedido.id,
    estado_desde="EN_CAMINO",
    estado_a="ENTREGADO",
    timestamp=datetime.now()
)
uow.historial_estado.add(historial)
await uow.commit()
```

## State Management

### Zustand (Client State)
For state that lives on the client:

```typescript
import { create } from 'zustand'

export const useCartStore = create((set) => ({
  items: [],
  addItem: (product) => set((state) => ({
    items: [...state.items, product]
  })),
  clear: () => set({ items: [] })
}))
```

### TanStack Query (Server State)
For data from the backend:

```typescript
const { data: products } = useQuery({
  queryKey: ['products'],
  queryFn: () => api.getProducts()
})
```

**Never mix:** Don't store server data in Zustand.

## Naming Conventions

### Backend (Python)
- **Modules**: `snake_case` — `auth/`, `usuarios/`, `productos/`
- **Classes**: `PascalCase` — `Usuario`, `Producto`, `Pedido`
- **Functions**: `snake_case` — `get_user()`, `create_product()`
- **Tables**: `snake_case` — `usuario`, `producto`, `pedido`
- **Schemas**: `PascalCase` — `UsuarioCreate`, `UsuarioRead`, `UsuarioUpdate`

### Frontend (TypeScript)
- **Components**: `PascalCase` — `LoginForm`, `ProductCard`, `OrderDetail`
- **Hooks**: `camelCase` with `use` prefix — `useLogin()`, `useProducts()`, `useCart()`
- **Stores**: `camelCase` with `Store` suffix — `authStore`, `cartStore`, `uiStore`
- **Types**: `PascalCase` — `User`, `Product`, `Order`
- **Functions**: `camelCase` — `formatPrice()`, `isValidEmail()`
- **Directories**: `kebab-case` — `shared/ui/`, `features/auth/`

## Testing

### Backend
Write tests in `backend/tests/`:

```python
async def test_register_user(uow: UnitOfWork):
    await auth_service.register_user(uow, "test@example.com", "password")
    user = await uow.usuarios.get_by_email("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"
```

### Frontend
Write tests in `frontend/src/**/__tests__/`:

```typescript
import { render, screen } from '@testing-library/react'
import { LoginForm } from './LoginForm'

test('renders login form', () => {
  render(<LoginForm />)
  expect(screen.getByText('Login')).toBeInTheDocument()
})
```

## Error Handling

### Backend: RFC 7807 Problem Detail
Use custom exceptions:

```python
from app.core.exceptions import ResourceNotFound

class UsuarioNotFound(ResourceNotFound):
    def __init__(self, user_id: int):
        super().__init__(
            detail=f"Usuario {user_id} no encontrado",
            resource_type="usuario",
            resource_id=user_id
        )

# Raises:
# {
#   "type": "https://example.com/errors/resource-not-found",
#   "title": "Resource Not Found",
#   "status": 404,
#   "detail": "Usuario 123 no encontrado",
#   "instance": "/api/v1/usuarios/123"
# }
```

### Frontend: Error Boundaries
Wrap risky components:

```typescript
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <OrdersList />
</ErrorBoundary>
```

## Code Review Checklist

### Backend PR
- [ ] Follows Router → Service → UoW → Repository → Model flow
- [ ] No circular imports
- [ ] Exceptions use RFC 7807 format
- [ ] All endpoints have tests
- [ ] Database operations use UoW
- [ ] Type hints on all functions
- [ ] Docstrings on public functions

### Frontend PR
- [ ] Features don't import from other features
- [ ] Components use TypeScript strict mode
- [ ] No `any` types (unless absolutely necessary)
- [ ] Zustand for client state, TanStack Query for server state
- [ ] Components tested with React Testing Library
- [ ] No console logs in production code
- [ ] Tailwind classes (no CSS files)

## Performance Guidelines

### Backend
- Use database indexes on frequently queried fields
- Batch queries when possible (avoid N+1)
- Cache with Redis if appropriate
- Use async/await, not blocking calls

### Frontend
- Lazy-load routes with `React.lazy()`
- Memoize expensive computations
- Use `React.memo()` for pure components
- Virtualize long lists

## Deployment

Handled in a future change. For now, focus on development.

## Getting Help

1. **Architecture question?** → Read `docs/Integrador.txt`
2. **Setup issue?** → Check `backend/README.md` or `frontend/README.md`
3. **Domain logic question?** → Check `docs/Historias_de_usuario.txt`
4. **Change details?** → Check `openspec/changes/<change-name>/design.md`

---

**Happy coding! 🚀**
