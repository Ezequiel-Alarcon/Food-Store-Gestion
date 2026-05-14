## Why

El Change 16 (`users-admin` — backend) implementó los endpoints CRUD de usuarios (`GET /api/v1/usuarios`, `PUT /api/v1/usuarios/:id`, `PATCH /api/v1/usuarios/:id/estado`) pero no existe panel frontend para que ADMIN interactúe con ellos. El Change 21 completa ese change con la interfaz de gestión de usuarios.

## What Changes

- Nueva página `/admin/usuarios` con tabla de usuarios (nombre, email, rol, estado, fecha registro)
- Búsqueda por nombre o email
- Filtro por rol
- Paginación
- Modal/edición inline para cambiar rol de usuario
- Toggle para activar/desactivar usuario
- Indicador visual del último ADMIN (protección RN-RB04)
- Navegación actualizada en Navigation.tsx para ADMIN

## Capabilities

### New Capabilities
- `admin-users-ui`: Panel de administración de usuarios para ADMIN con tabla, búsqueda, filtros, edición de rol y toggle de estado.

### Modified Capabilities
- _(ninguna — el backend ya existe y no cambia)_

## Impact

- **Archivos nuevos:** `frontend/src/entities/usuario-admin/`, `frontend/src/features/admin/users/`
- **Archivos modificados:** `frontend/src/features/layout/Navigation.tsx`, `frontend/src/providers/RouterProvider.tsx`
- **Backend consumido:** `GET /api/v1/usuarios`, `PUT /api/v1/usuarios/:id`, `PATCH /api/v1/usuarios/:id/estado`
- **Dependencias:** Change 16 (`users-admin` backend) debe estar archivado