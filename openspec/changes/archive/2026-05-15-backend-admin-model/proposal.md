## Why

El módulo `admin` tiene `model.py` vacío, `AdminRepository` no sigue el patrón `BaseRepository[T]`, y `AdminService` crea sesiones directamente bypassando Unit of Work. Esto viola la convención arquitectónica del proyecto (`Router → Service → UoW → Repository → Model`). Además, varios endpoints construyen dicts inline sin schemas Pydantic y las queries de métricas no soportan filtros por rango de fechas como especifican las historias de usuario originales.

## What Changes

- Completar `model.py` con re-exports centralizados de modelos que admin consulta (`Pedido`, `Producto`, `Usuario`, `DetallePedido`, `HistorialEstadoPedido`)
- Refactorizar `AdminRepository` para heredar de `BaseRepository` o al menos seguir el patrón de inyección de sesión consistente
- Refactorizar `AdminService` para usar Unit of Work en lugar de crear `SessionLocal()` directamente
- Agregar filtros por rango de fechas en queries de métricas (`desde`, `hasta`)
- Crear schemas Pydantic para endpoints de detalle de pedido que actualmente usan dicts inline
- Agregar query de total de usuarios registrados (HU US-056)

## Capabilities

### New Capabilities
- `admin-model-queries`: Queries reutilizables del módulo admin con soporte de filtros temporales, centralizadas en repository con patrón `BaseRepository`.

### Modified Capabilities
- `admin-metrics`: Las métricas existentes ahora soportan filtros por rango de fechas (`desde`, `hasta`) como parámetros opcionales de query. El comportamiento sin filtros se mantiene igual (backward compatible).

## Impact

- **Backend**: `backend/app/modules/admin/model.py` (nuevo contenido), `repository.py` (refactor), `service.py` (refactor UoW + nuevos métodos), `schemas.py` (nuevos schemas), `router.py` (schemas de respuesta para pedidos)
- **API**: Endpoints existentes mantienen compatibilidad — los filtros de fecha son parámetros opcionales
- **Tests**: Nuevos tests unitarios para repository y service
- **Frontend**: Sin cambios — los endpoints existentes siguen funcionando igual
