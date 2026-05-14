## Why

El backend del change 15 (`orders-list-gestor`) ya está implementado y archivado, exponiendo los endpoints para que gestores y admins puedan listar y ver detalles de cualquier pedido. Ahora necesitamos el frontend para que estos usuarios puedan interactuar con esa funcionalidad desde la interfaz web.

## What Changes

- **Nueva página**: Panel de pedidos para gestor/admin en `/admin/pedidos`
- **Componente de lista**: Tabla con filtros por estado, búsqueda por cliente, paginación
- **Componente de detalle**: Vista completa del pedido con items, dirección, timeline de estados
- **Integración con API**: Consumo de endpoints `/api/v1/admin/pedidos` y `/api/v1/admin/pedidos/{id}`
- **Navegación**: Acceso desde el menú admin (gestores y admins ven esta opción)

## Capabilities

### New Capabilities
- `orders-list-gestor-ui`: Panel de pedidos para gestores y admins — lista filtrable + detalle de pedido

### Modified Capabilities
- Ninguno — es frontend puro, no modifica requisitos del backend

## Impact

- **Frontend**: Nuevos archivos en `frontend/src/features/admin/orders/`
- **Routing**: Nueva ruta `/admin/pedidos` y `/admin/pedidos/:id`
- **Store**: Utiliza existentes — authStore para verificar rol, no requiere store nuevo
- **Dependencias**: Depende del backend `orders-list-gestor` (change 15) ya archivado