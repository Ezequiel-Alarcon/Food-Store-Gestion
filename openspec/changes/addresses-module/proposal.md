## Why

Hoy el sistema no tiene un módulo formal de direcciones para (a) usuarios (envíos) y (b) sucursales (puntos de retiro). Esto bloquea flujos básicos (guardar múltiples direcciones, elegir predeterminada, mostrar sucursales) y deja reglas ambiguas entre frontend y backend.

## What Changes

- Agregar módulo de **direcciones de usuario** con soporte de:
  - múltiples direcciones por usuario
  - una dirección **predeterminada** por usuario
  - CRUD (crear/editar/eliminar/listar) y selección de predeterminada
- Agregar módulo de **direcciones de sucursal** (punto de retiro) con CRUD y listado.
- Normalizar el modelo de “Address” como **texto** (sin lat/lng).
- Exponer endpoints backend y contratos frontend para consumirlos.

## Capabilities

### New Capabilities

- `user-addresses`: gestión de direcciones de envío del usuario (múltiples + predeterminada)
- `branch-addresses`: gestión de direcciones de sucursales (puntos de retiro)

### Modified Capabilities

- (ninguna por ahora)

## Impact

- Backend: nuevos módulos para direcciones (usuarios y sucursales), modelos/tablas, repos/services/routers y permisos (RBAC).
- Frontend: features/entities para CRUD/listado/selección y consumo vía `api.ts`.
- DB/Alembic: migraciones para tablas de direcciones y constraints (p.ej. “una predeterminada por usuario”).
