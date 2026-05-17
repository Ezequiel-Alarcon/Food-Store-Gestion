## 1. Entities — API client, types y queries

- [x] 1.1 Crear `entities/perfil/types.ts` con interfaces `PerfilResponse`, `UpdateProfileRequest`, `ChangePasswordRequest` y `MessageResponse`
- [x] 1.2 Crear `entities/perfil/api.ts` con `perfilApi` (métodos `getPerfil`, `updatePerfil`, `changePassword`)
- [x] 1.3 Crear `entities/perfil/queries.ts` con `usePerfil` (query), `useUpdatePerfil` (mutation) y `useChangePassword` (mutation)
- [x] 1.4 Crear `entities/perfil/index.ts` barrel file con re-exports

## 2. ProfilePage — Página de perfil

- [x] 2.1 Crear `pages/ProfilePage.tsx` con sección de datos personales (card con info actual + botón "Editar" que despliega formulario inline)
- [x] 2.2 Agregar sección de cambio de contraseña (formulario independiente con campos current_password y new_password)
- [x] 2.3 Manejar estados: loading (skeleton/spinner), error (mensaje + retry), success (toast/mensaje verde) para cada operación

## 3. Routing y navegación

- [x] 3.1 Agregar ruta `/perfil` en `providers/RouterProvider.tsx` con `ProtectedRoute` (sin restricción de roles — cualquier usuario autenticado)
- [x] 3.2 Agregar ítem "Mi Perfil" (`{ label: 'Mi Perfil', href: '/perfil' }`) en el array `CLIENT` de `MENU_BY_ROLE` en `features/layout/Navigation.tsx`
