## Context

El backend expone endpoints CRUD completos para sucursales (`/branches`) y sus direcciones (`/branches/{branchId}/address`), protegidos con `require_role("ADMIN")`. El frontend ya tiene `branchAddressesApi` con `create/update/remove` en `entities/addresses/api.ts` y una query `useBranchAddresses` en `entities/addresses/queries.ts`. Sin embargo, no existe ninguna UI para que ADMIN cree o gestione sucursales — la página `/puntos-retiro` (`PickupPointsPage`) es solo lectura.

Este design cubre exclusivamente el frontend. Cero cambios en backend.

## Goals / Non-Goals

**Goals:**
- Página `/admin/sucursales` con tabla de sucursales existentes (nombre, dirección asociada, estado)
- Modal/formulario para crear sucursal con su dirección
- Modal/formulario para editar sucursal (nombre, dirección)
- Eliminar sucursal (soft-delete/reactivar)
- Reutilizar `branchAddressesApi` y `useBranchAddresses` existentes
- Seguir patrón FSD: `features/admin/sucursales/`

**Non-Goals:**
- No se modifica el backend
- No se modifica la página pública `/puntos-retiro` (`PickupPointsPage`)
- No se agregan nuevos endpoints ni schemas
- No se modifica el modelo de datos

## Decisions

### 1. Estructura FSD: `features/admin/sucursales/`

Se sigue el mismo patrón que los otros módulos admin (`features/admin/products/`, `features/admin/categories/`, `features/admin/stock/`):

```
features/admin/sucursales/
├── SucursalesPage.tsx     # Página principal con tabla
├── SucursalFormModal.tsx  # Modal de crear/editar sucursal
└── index.ts               # Barrel export
```

**Alternativa considerada:** `features/admin/pickup-points/` — descartado porque el backend ya usa el concepto "sucursales" (branches), y mantener consistencia de naming.

### 2. Reutilizar API client existente

Se usan `branchAddressesApi` (ya existente en `entities/addresses/api.ts`) y se agrega un nuevo `branchesApi` para el CRUD de sucursales (list, create, update, delete).

Los endpoints del backend ya expuestos:
- `GET /branches/` → listar sucursales activas
- `POST /branches/` → crear sucursal (solo nombre)
- `PATCH /branches/{id}` → editar sucursal (nombre, activa)
- `GET /branches/{id}/address` → obtener dirección de sucursal
- `POST /branches/{id}/address` → crear dirección de sucursal
- `PATCH /branches/{id}/address` → actualizar dirección
- `DELETE /branches/{id}/address` → eliminar dirección

### 3. Flujo de creación: sucursal + dirección en un solo paso

Al crear una sucursal, el formulario incluye tanto el nombre de la sucursal como su dirección. Internamente se hacen dos requests secuenciales:
1. `POST /branches` → crea la sucursal, devuelve `{ id }`
2. `POST /branches/{id}/address` → crea la dirección asociada

Si falla el paso 2, se muestra error y se sugiere editar la sucursal para agregar dirección.

### 4. Tabla con datos enriquecidos

La tabla de sucursales necesita mostrar el nombre de la sucursal Y su dirección. Se usan dos queries paralelas con TanStack Query:
- `useQuery(['branches'])` → `GET /branches/`
- `useQuery(['branch-addresses'])` → `GET /branches/addresses` (ya existe)

Se hace merge client-side por `branch_id` para mostrar la dirección junto a cada sucursal.

### 5. Navegación protegida

La ruta `/admin/sucursales` se protege con `ProtectedRoute` (rol ADMIN). Se agrega "Sucursales" al array `ADMIN` en `Navigation.tsx`.

### 6. Sin página de gestión separada para direcciones

No se crea una página separada solo para gestionar direcciones. Cada sucursal tiene exactamente una dirección (relación 1:1 en la práctica), así que el formulario de sucursal incluye los campos de dirección. Esto simplifica la UI y evita sobre-ingeniería.

## Risks / Trade-offs

- **[Riesgo bajo] Race condition en creación**: Si dos admins crean sucursales simultáneamente, no hay problema — los nombres no tienen constraint UNIQUE.
- **[Trade-off] Sin página de direcciones separada**: Si en el futuro una sucursal necesita múltiples direcciones, habrá que refactorizar. Por ahora es 1:1, así que el diseño actual es adecuado.
- **[Riesgo bajo] Sucursales sin dirección**: El formulario de creación incluye dirección obligatoria, pero si se crea una sucursal y falla la dirección, queda una sucursal "huérfana". Se mitiga con mensaje claro al admin y opción de editar.
