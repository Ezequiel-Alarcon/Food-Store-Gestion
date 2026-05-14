## Context

El Change 16 (`users-admin`) dejó listos los endpoints de gestión de usuarios en backend. Ahora se construye la interfaz frontend para ADMIN. El código base ya tiene una estructura admin (`frontend/src/features/admin/orders/`) que sirve de referencia para seguir los mismos patrones.

## Goals / Non-Goals

**Goals:**
- Tabla de usuarios con columnas: nombre, email, rol, estado, fecha de registro
- Búsqueda por nombre o email (input con debounce)
- Filtro por rol (dropdown)
- Paginación
- Editar rol de usuario via modal con dropdown de roles
- Toggle activar/desactivar usuario
- Protección visual del último ADMIN del sistema

**Non-Goals:**
- No implementar nuevos endpoints de backend
- No modificar el modelo de datos
- No crear usuarios nuevos (solo editar existentes)
- No implementar gestión de usuarios para STOCK o PEDIDOS (solo ADMIN)

## Decisions

### 1. Estructura de archivos (FSD)

`frontend/src/entities/usuario-admin/` — tipos + API client para los endpoints de usuarios.
`frontend/src/features/admin/users/ui/` — página UsersPage + componentes reutilizables.

**Alternativa descartada:** meter todo en un solo archivo. Se sigue FSD para consistencia con `orders-list-gestor-frontend`.

### 2. Estado del servidor con TanStack Query

Los datos de usuarios se gestionan exclusivamente con TanStack Query (query + mutation). Estado local (filtros, búsqueda) en `useState`.

**Alternativa descartada:** Zustand. Los estados de servidor no van en stores de cliente por convención del proyecto.

### 3. Edición de rol via modal

Se usa un modal con dropdown de roles en vez de edición inline para evitar modificaciones accidentales y dejar claro qué se está cambiando.

**Alternativa descartada:** edición inline — menos control y más riesgo de cambios por error.

### 4. Protección último ADMIN

El endpoint `PUT /api/v1/usuarios/:id` valida RN-RB04 en backend. El frontend muestra un badge/indicador visual cuando el usuario que se está editando es el último ADMIN y es uno mismo.

## Risks / Trade-offs

- **Riesgo:** El endpoint de listar usuarios no tiene búsqueda/filtro en backend (soquetes en query params). **Mitigación:** filtrar en frontend lado cliente (aceptable para datasets de gestión admin pequeños).
- **Riesgo:** El rol del usuario actual cambia tras editarse a sí mismo. **Mitigación:** TanStack Query invalidate queries post-mutation para forzar re-fetch del auth state.