# tasks.md -- addresses-module

## 1. Backend: modelos + migraciones

- [x] 1.1 Crear modelos SQLModel para `user_addresses` y `branch_addresses` (campos textuales + `activa`, `is_default` en user)
- [x] 1.2 Agregar relaciones/FKs: `user_addresses.user_id` y `branch_addresses.branch_id`
- [x] 1.3 Crear migración Alembic para ambas tablas
- [x] 1.4 Agregar índice único parcial: `UNIQUE (user_id) WHERE is_default = true AND activa = true`
- [x] 1.5 Agregar constraint/índice para `branch_id` (1 address activa por sucursal) y definir comportamiento (reemplazar vs 409)

## 2. Backend: repos + services (Router→Service→UoW→Repo)

- [x] 2.1 Crear repositorios: `UserAddressRepository`, `BranchAddressRepository` (BaseRepository)
- [x] 2.2 Crear services para CRUD (validaciones de ownership y activa)
- [x] 2.3 Implementar operación atómica `set_default_address(user_id, address_id)` usando UoW

## 3. Backend: routers + RBAC

- [x] 3.1 Router user addresses:
  - [x] GET `/api/v1/user/addresses`
  - [x] POST `/api/v1/user/addresses`
  - [x] PATCH `/api/v1/user/addresses/{id}`
  - [x] DELETE `/api/v1/user/addresses/{id}` (soft-delete)
  - [x] POST `/api/v1/user/addresses/{id}/default`
- [x] 3.2 Enforzar: solo el usuario dueño puede ver/modificar
- [x] 3.3 Router branch addresses:
  - [x] GET `/api/v1/branches/addresses`
  - [x] POST/PATCH/DELETE `/api/v1/branches/{branchId}/address` (ADMIN o rol equivalente)
- [x] 3.4 Errores consistentes: 404 no existe, 403 no permitido, 409 conflicto (default inactiva / duplicados)

## 4. Frontend: API + store/query

- [x] 4.1 Agregar client/funciones para user addresses (list/create/update/delete/setDefault)
- [x] 4.2 Agregar client/funciones para branch addresses (list, admin create/update/delete)
- [x] 4.3 Integrar con `api.ts` existente (auth header + refresh ya está)

## 5. Frontend: UI mínima

- [x] 5.1 Página/feature “Mis direcciones” (listar + crear/editar/eliminar)
- [x] 5.2 Acción “Marcar como predeterminada” (y reflejar visualmente)
- [x] 5.3 Listado de sucursales/puntos de retiro (solo lectura) usando branch addresses

## 6. Verificación (manual)

- [ ] 6.1 Verificar CRUD user addresses end-to-end (incluye ownership)
- [ ] 6.2 Verificar set default: siempre queda una sola default activa
- [ ] 6.3 Verificar branch addresses: listado + RBAC de admin

> Nota: por convención del proyecto, NO correr build/tests automáticamente.

## Notas de verificación manual

- User addresses:
  - Login como CLIENT
  - Ir a `/direcciones`
  - Crear/editar/eliminar y marcar default; verificar que al marcar default se desmarca la anterior
- Branch addresses:
  - Como ADMIN: crear una `Sucursal` (opcional) y luego POST `/api/v1/branches/{id}/address`
  - Verificar que un segundo POST para la misma sucursal reemplaza (soft-delete) la dirección activa
  - Como usuario no admin: intentar POST/PATCH/DELETE y esperar 403
