## 1. API Client & Types

- [x] 1.1 Crear `frontend/src/entities/usuario-admin/types.ts` — interfaces: UserAdmin, UserListResponse
- [x] 1.2 Crear `frontend/src/entities/usuario-admin/api.ts` — cliente API para GET /usuarios, PUT /usuarios/:id, DELETE /usuarios/:id

## 2. Users List Page

- [x] 2.1 Crear `frontend/src/features/admin/users/ui/UsersPage.tsx` — página principal con tabla
- [x] 2.2 Tabla con columnas: Nombre, Email, Rol, Estado, Fecha de Registro, Acciones
- [x] 2.3 Crear `SearchInput.tsx` — input de búsqueda con debounce
- [x] 2.4 Crear `RoleFilter.tsx` — dropdown para filtrar por rol
- [x] 2.5 Paginación implementada en UsersPage
- [x] 2.6 Skeleton loaders implementados
- [x] 2.7 Empty state: "No se encontraron usuarios"
- [x] 2.8 Error state con botón "Reintentar"

## 3. Edit User Modal

- [x] 3.1 Crear `EditUserModal.tsx` — modal con dropdown de roles (ADMIN, STOCK, PEDIDOS, CLIENT)
- [x] 3.2 Protección último ADMIN: warning + botón deshabilitado si aplica
- [x] 3.3 Integrar modal en UsersPage (botón de editar por fila)
- [x] 3.4 Toast de éxito al guardar

## 4. Toggle User Status

- [x] 4.1 Botón activar/desactivar en columna Acciones (color según estado)
- [x] 4.2 Confirmación antes de toggle (modal simple)
- [x] 4.3 Toast de éxito/error post-toggle

## 5. Routing & Navigation

- [x] 5.1 Ruta `/admin/usuarios` en RouterProvider.tsx
- [x] 5.2 Rutas protegidas con ProtectedRoute (solo rol ADMIN)
- [x] 5.3 Link "Gestión de Usuarios" en Navigation.tsx para ADMIN (ya existente)

## 6. Testing

- [ ] 6.1 Verificar que la página carga con usuarios
- [ ] 6.2 Verificar búsqueda funciona (nombre + email)
- [ ] 6.3 Verificar filtro por rol funciona
- [ ] 6.4 Verificar edición de rol (modal + save)
- [ ] 6.5 Verificar toggle activar/desactivar