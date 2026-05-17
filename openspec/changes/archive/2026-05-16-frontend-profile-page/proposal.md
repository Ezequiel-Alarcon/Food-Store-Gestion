## Why

El frontend no tiene página de perfil. El backend expone 3 endpoints (`GET/PUT /api/v1/perfil`, `PUT /api/v1/perfil/password`) listos desde la Fase 1, pero no hay forma de que un usuario vea o edite sus datos desde la UI. Esto deja huérfanas las HU US-061 (ver perfil propio), US-062 (editar perfil propio) y US-063 (cambiar contraseña) del lado del cliente.

## What Changes

- Se crea `entities/perfil/` con API client, tipos TypeScript y queries de TanStack Query para los 3 endpoints de perfil
- Se crea `pages/ProfilePage.tsx` con dos secciones: formulario de edición de datos personales (nombre, apellido, teléfono) y formulario de cambio de contraseña
- Se agrega la ruta `/perfil` en `RouterProvider.tsx`, protegida para cualquier usuario autenticado
- Se agrega el ítem "Mi Perfil" en el menú de navegación para el rol CLIENT (`Navigation.tsx`)

## Capabilities

### New Capabilities
- `profile-management`: Ver, editar datos personales y cambiar contraseña del usuario autenticado desde el frontend

### Modified Capabilities
<!-- Ninguna — es funcionalidad nueva que no modifica specs existentes -->

## Impact

- **Nuevos archivos (~4):** `entities/perfil/api.ts`, `entities/perfil/types.ts`, `entities/perfil/queries.ts`, `entities/perfil/index.ts`, `pages/ProfilePage.tsx`
- **Archivos modificados (~2):** `providers/RouterProvider.tsx` (ruta), `features/layout/Navigation.tsx` (menú)
- **Dependencias:** Backend `perfil` module (ya implementado), `lib/api.ts` (Axios instance), TanStack Query
- **Sin impacto en backend ni base de datos**
