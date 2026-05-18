## 1. API Client — Branches Endpoints

- [x] 1.1 Agregar `branchesApi` en `frontend/src/entities/addresses/api.ts` con métodos `list`, `create`, `update`, `remove` para los endpoints `/branches/` y `/branches/{id}`
- [x] 1.2 Agregar tipos TypeScript `Branch` y `BranchCreate`/`BranchUpdate` en `frontend/src/entities/addresses/types.ts` (o en archivo nuevo si es necesario)

## 2. TanStack Query — Hooks para Branches

- [x] 2.1 Agregar `useBranches()` query en `frontend/src/entities/addresses/queries.ts`
- [x] 2.2 Agregar `useCreateBranch()`, `useUpdateBranch()`, `useDeleteBranch()` mutations
- [x] 2.3 Agregar `useCreateBranchAddress()`, `useUpdateBranchAddress()`, `useDeleteBranchAddress()` mutations (wrapper de `branchAddressesApi` existente)

## 3. Feature — SucursalFormModal

- [x] 3.1 Crear `frontend/src/features/admin/sucursales/SucursalFormModal.tsx`
- [x] 3.2 Implementar formulario con campos: nombre sucursal + dirección (calle, número, piso/depto, ciudad, provincia, CP, país, referencias)
- [x] 3.3 Soporte dual crear/editar: al editar precarga datos existentes de sucursal y dirección
- [x] 3.4 Flujo de creación: POST `/branches` → con ID resultante → POST `/branches/{id}/address`
- [x] 3.5 Flujo de edición: PATCH `/branches/{id}` + PATCH `/branches/{id}/address`
- [x] 3.6 Validación frontend: nombre obligatorio, calle obligatoria, número numérico, CP numérico
- [x] 3.7 Mostrar errores del backend usando `response.data.detail`

## 4. Feature — SucursalesPage

- [x] 4.1 Crear `frontend/src/features/admin/sucursales/SucursalesPage.tsx`
- [x] 4.2 Tabla con columnas: Nombre, Dirección, Estado (activa/inactiva), Acciones (Editar, Eliminar)
- [x] 4.3 Merge client-side de branches + branch-addresses para mostrar dirección por sucursal
- [x] 4.4 Botón "Nueva sucursal" que abre SucursalFormModal
- [x] 4.5 Botón "Editar" que abre SucursalFormModal con datos precargados
- [x] 4.6 Botón "Eliminar" con confirmación via `openConfirmModal`
- [x] 4.7 Estados: loading (skeleton), error (retry), empty (mensaje)
- [x] 4.8 Toast de éxito/error en cada operación

## 5. Barrel Export

- [x] 5.1 Crear `frontend/src/features/admin/sucursales/index.ts` exportando `SucursalesPage`

## 6. Routing

- [x] 6.1 Agregar ruta protegida en `frontend/src/providers/RouterProvider.tsx`

## 7. Navigation

- [x] 7.1 Agregar item `{ label: 'Sucursales', href: '/admin/sucursales' }` al array `ADMIN` en `frontend/src/features/layout/Navigation.tsx`
