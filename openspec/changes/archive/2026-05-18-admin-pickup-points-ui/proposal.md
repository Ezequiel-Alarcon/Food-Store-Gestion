## Why

Actualmente los puntos de retiro (sucursales y sus direcciones) solo pueden crearse/editars/eliminarse desde el backend o herramientas externas. El administrador no tiene ninguna interfaz en el frontend para gestionarlos — la página `/puntos-retiro` es de solo lectura para todos los roles. Esto obliga a crear sucursales manualmente desde la base de datos o la API, lo cual es inviable en producción.

El backend ya expone todos los endpoints necesarios con RBAC (solo ADMIN), y el API client del frontend ya tiene las funciones `branchAddressesApi.create/update/remove`. Solo falta la UI.

## What Changes

- Nueva página de gestión de sucursales en `/admin/sucursales` (protegida, solo ADMIN)
- CRUD completo de sucursales: crear, editar nombre/dirección, eliminar (soft-delete/reactivar)
- CRUD de direcciones de sucursal asociadas
- La página pública `/puntos-retiro` sigue siendo de solo lectura para clientes
- Se agrega "Sucursales" al menú de navegación para ADMIN
- Validación frontend en formularios de sucursal y dirección

## Capabilities

### New Capabilities

- `admin-pickup-points`: Interfaz de administración para que ADMIN gestione sucursales (crear, editar, eliminar) y sus direcciones de punto de retiro asociadas.

### Modified Capabilities

- `branch-addresses`: Se extiende con la nueva UI de administración. Las specs de branch-addresses actualmente solo cubren la API pública de lectura. Se agregan los endpoints de escritura (ya implementados en backend) y la UI admin correspondiente.

## Impact

- **Backend**: Sin cambios — todos los endpoints ya existen con RBAC correcto (`require_role("ADMIN")`)
- **Frontend**: Nueva página `features/admin/sucursales/`, ruta protegida en `RouterProvider.tsx`, item en menú de `Navigation.tsx`
- **API Client**: `entities/addresses/api.ts` ya tiene `branchAddressesApi.create/update/remove` — solo se usan donde antes no se usaban
- **Seguridad**: Sin cambios — el backend ya protege los endpoints de escritura con `require_role("ADMIN")`
