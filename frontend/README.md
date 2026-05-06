# Food Store Frontend

## Overview

The Food Store frontend is a React TypeScript application built with Vite. It implements **Feature-Sliced Design (FSD)**, a scalable architecture that organizes code into horizontal layers with vertical feature slices.

## Directory Structure

```
frontend/
├── src/
│   ├── app/                  # App-level providers and configuration
│   │   ├── App.tsx           # Root component
│   │   ├── providers/        # React Query, Router, Theme providers
│   │   ├── router/           # Route definitions
│   │   └── __init__.ts
│   │
│   ├── pages/                # Page components (one per route)
│   │   ├── HomePage.tsx
│   │   ├── ProductsPage.tsx
│   │   ├── OrdersPage.tsx
│   │   ├── AdminDashboard.tsx
│   │   └── __init__.ts
│   │
│   ├── features/             # Feature modules (isolated user interactions)
│   │   ├── auth/
│   │   │   ├── components/   # LoginForm, RegisterForm
│   │   │   ├── hooks/        # useAuth, useLogin
│   │   │   ├── stores/       # authStore (Zustand)
│   │   │   ├── index.ts      # Public exports
│   │   │   └── __init__.ts
│   │   │
│   │   ├── cart/
│   │   │   ├── components/   # CartDrawer, CartSummary
│   │   │   ├── hooks/        # useCart
│   │   │   ├── stores/       # cartStore (Zustand)
│   │   │   ├── index.ts
│   │   │   └── __init__.ts
│   │   │
│   │   ├── orders/
│   │   │   ├── components/   # OrdersList, OrderDetail
│   │   │   ├── hooks/        # useOrders
│   │   │   ├── api/          # API calls for orders
│   │   │   ├── index.ts
│   │   │   └── __init__.ts
│   │   │
│   │   └── admin/
│   │       ├── components/   # Dashboard, UserManagement
│   │       ├── hooks/        # useMetrics, useUsers
│   │       ├── api/          # Admin endpoints
│   │       ├── index.ts
│   │       └── __init__.ts
│   │
│   ├── entities/             # Domain models and data layer
│   │   ├── models/           # User, Product, Order TypeScript types
│   │   ├── api/              # Axios clients, API calls
│   │   │   ├── client.ts     # Axios instance with interceptors
│   │   │   ├── products.ts   # Product API calls
│   │   │   ├── orders.ts     # Order API calls
│   │   │   └── auth.ts       # Auth API calls
│   │   ├── hooks/            # Shared hooks (useQuery, useMutation)
│   │   ├── index.ts
│   │   └── __init__.ts
│   │
│   ├── shared/               # Shared across features (no business logic)
│   │   ├── ui/               # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── lib/              # Utilities, helpers, constants
│   │   │   ├── api.ts        # API client setup
│   │   │   ├── constants.ts  # App constants
│   │   │   ├── utils.ts      # Helper functions
│   │   │   ├── hooks/        # Shared hooks (useIsMobile, etc.)
│   │   │   └── index.ts
│   │   │
│   │   ├── types/            # Global TypeScript types
│   │   │   ├── api.ts        # API response types
│   │   │   ├── models.ts     # Domain models
│   │   │   └── index.ts
│   │   │
│   │   ├── stores/           # Global Zustand stores
│   │   │   ├── uiStore.ts    # UI state (modals, sidebar)
│   │   │   ├── paymentStore.ts  # Payment flow state
│   │   │   └── index.ts
│   │   │
│   │   └── __init__.ts
│   │
│   ├── main.tsx              # React entry point
│   ├── index.css             # Global styles
│   └── __init__.ts
│
├── public/                   # Static assets
│   └── favicon.svg
│
├── .env.example              # Environment variables template
├── package.json              # Dependencies
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript configuration
├── tailwind.config.ts        # Tailwind configuration
├── postcss.config.js         # PostCSS configuration
├── README.md
└── .gitignore
```

## Architecture: Feature-Sliced Design (FSD)

FSD organizes code into layers, with imports flowing **downward only**:

```
app (providers, routing)
  ↓ imports from
pages (route components)
  ↓ imports from
features (user interactions)
  ↓ imports from
entities (domain models, API)
  ↓ imports from
shared (UI components, utilities)
```

**Golden rule**: A feature NEVER imports from another feature or from layers above it. Pages never import from pages.

## Import Examples

✅ **Correct**:
```typescript
// In feature/auth/components/LoginForm.tsx
import { Button, Input } from '@/shared/ui'
import { useLogin } from '@/feature/auth/hooks'
import { User } from '@/entities/models'
```

❌ **Wrong**:
```typescript
// In feature/auth/components/LoginForm.tsx
import { CartDrawer } from '@/features/cart'  // ❌ Features don't import from each other
import { HomePage } from '@/pages'             // ❌ Features don't import from pages
```

## Feature Module Template

Each feature should have this structure:

```typescript
// feature/myfeature/index.ts - Public API
export { MyFeatureComponent } from './components'
export { useMyFeature } from './hooks'
export { myFeatureStore } from './stores'

// feature/myfeature/components/MyComponent.tsx
export const MyComponent = () => {
  // Component code
}

// feature/myfeature/hooks/useMyFeature.ts
export const useMyFeature = () => {
  // Hook logic
}

// feature/myfeature/stores/myFeatureStore.ts
import { create } from 'zustand'
export const myFeatureStore = create((set) => ({
  // Zustand store
}))
```

## State Management

### Zustand (Client State)
For local state that doesn't sync with the server:
- Cart items
- UI state (modals, sidebar visibility)
- Form state (user preferences)
- Authentication status (locally)

```typescript
import { create } from 'zustand'

export const useCartStore = create((set) => ({
  items: [],
  addItem: (product) => set((state) => ({
    items: [...state.items, product]
  }))
}))
```

### TanStack Query (Server State)
For data from the backend:
- Products list
- User profile
- Orders
- Dashboard metrics

```typescript
import { useQuery } from '@tanstack/react-query'
import { getProducts } from '@/entities/api'

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: getProducts
  })
}
```

### Never Mix
❌ Don't put server data in Zustand:
```typescript
// WRONG
const useStore = create((set) => ({
  products: []  // ❌ Should use useQuery instead
}))
```

## API Communication

All API calls live in `entities/api/`:

```typescript
// entities/api/products.ts
import { client } from './client'

export const getProducts = async () => {
  const { data } = await client.get('/api/v1/products')
  return data
}

export const getProductById = async (id: number) => {
  const { data } = await client.get(`/api/v1/products/${id}`)
  return data
}
```

The Axios client is configured in `entities/api/client.ts` with JWT interceptors and error handling.

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm or yarn

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with API_URL and other values
```

### 3. Run development server
```bash
npm run dev
```

App available at `http://localhost:5173`

### 4. Build for production
```bash
npm run build
npm run preview  # Test production build locally
```

## TypeScript Configuration

All files use strict mode (`strict: true`). No `any` types allowed without explicit `// @ts-ignore` comments (and good reason).

```typescript
// ✅ Good
const getName = (user: { name: string }): string => user.name

// ❌ Bad
const getName = (user: any): any => user.name
```

## Testing

Run tests with Vitest:

```bash
npm run test
npm run test:watch  # Watch mode
npm run test:coverage  # Coverage report
```

## Common Tasks

### Add a new feature
1. Create `frontend/src/features/myfeature/`
2. Add `components/`, `hooks/`, `stores/` subdirectories
3. Create public API in `index.ts`
4. Use in pages or other components (but not other features)

### Add a new page
1. Create `frontend/src/pages/MyPage.tsx`
2. Import features, entities, shared (never other pages)
3. Register route in `app/router/`

### Add a shared component
1. Create `frontend/src/shared/ui/MyComponent.tsx`
2. Export from `shared/ui/index.ts`
3. Use in any feature or page

### Fetch data from backend
1. Create API client in `entities/api/myfeature.ts`
2. Create hook in the feature or in `entities/hooks/`
3. Use `useQuery()` or `useMutation()` from TanStack Query

## Styling

Uses **Tailwind CSS** for all styles. No CSS-in-JS libraries.

```typescript
// ✅ Good
<button className="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded">
  Click me
</button>

// ❌ Bad (CSS Modules)
import styles from './Button.module.css'
<button className={styles.button}>Click me</button>
```

## Error Handling

Global error handling is set up in the Axios client. Add custom error boundaries as needed:

```typescript
import { ErrorBoundary } from 'react-error-boundary'

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <MyComponent />
</ErrorBoundary>
```

## Performance

- Routes are lazy-loaded using `React.lazy()`
- Images are optimized with responsive sizes
- Large lists use virtual scrolling (`react-window`)
- Components use `React.memo()` when appropriate

## Contributing

- Follow TypeScript strict mode
- Use Tailwind for styling (no CSS files)
- Create feature modules, not monolithic components
- Write hooks for complex logic
- Use TanStack Query for server state, Zustand for client state
- Add tests for new features
- Run linter before committing: `npm run lint`

---

**For architectural questions, see the main README at the project root.**
