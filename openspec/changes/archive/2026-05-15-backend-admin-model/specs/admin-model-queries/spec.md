## ADDED Requirements

### Requirement: Admin module has centralized model re-exports
El módulo admin SHALL tener un `model.py` que re-exporta los modelos de otros dominios que consulta: `Pedido`, `DetallePedido`, `Producto`, `Usuario`, `HistorialEstadoPedido`.

#### Scenario: Model imports are accessible
- **WHEN** otro módulo importa `from app.modules.admin.model import Pedido`
- **THEN** el import resuelve correctamente al modelo `Pedido` del módulo de pedidos

### Requirement: Admin queries support optional date filters
Las queries de métricas del módulo admin SHALL aceptar parámetros opcionales `desde` y `hasta` para filtrar por rango de fechas.

#### Scenario: Sales chart with date range
- **WHEN** un admin envía GET /api/v1/admin/metrics/sales-chart/?desde=2026-01-01&hasta=2026-01-31
- **THEN** el sistema devuelve datos de ventas solo para enero 2026

#### Scenario: Sales chart without date range (backward compatible)
- **WHEN** un admin envía GET /api/v1/admin/metrics/sales-chart/ sin parámetros
- **THEN** el sistema devuelve los últimos 30 días (comportamiento actual)

#### Scenario: Top products with date range
- **WHEN** un admin envía GET /api/v1/admin/metrics/top-products/?desde=2026-01-01&hasta=2026-01-31
- **THEN** el sistema devuelve top productos vendidos solo en enero 2026

#### Scenario: Orders by status with date range
- **WHEN** un admin envía GET /api/v1/admin/metrics/orders-by-status/?desde=2026-01-01
- **THEN** el sistema devuelve conteo de pedidos desde esa fecha

### Requirement: Admin can get total registered users count
El sistema SHALL permitir a un admin obtener el conteo total de usuarios registrados en el sistema.

#### Scenario: Get total users count
- **WHEN** un admin envía GET /api/v1/admin/metrics/
- **THEN** la respuesta incluye `total_usuarios` con el conteo de todos los usuarios registrados

### Requirement: Admin repository follows project patterns
El `AdminRepository` SHALL recibir la sesión de base de datos por inyección (desde el service o UoW), sin crear sesiones directamente.

#### Scenario: Repository receives session from service
- **WHEN** el service crea una instancia de AdminRepository
- **THEN** le pasa la sesión activa del UoW como parámetro

### Requirement: Admin service uses Unit of Work
El `AdminService` SHALL usar Unit of Work para todas sus operaciones, sin crear `SessionLocal()` directamente.

#### Scenario: Service wraps operations in UoW
- **WHEN** se llama a un método del service
- **THEN** la operación se ejecuta dentro de un contexto `with uow:`

### Requirement: Pedido detail endpoint uses typed schema
El endpoint GET /api/v1/admin/pedidos/{id}/ SHALL usar un `response_model` Pydantic tipado en lugar de construir un dict inline.

#### Scenario: Pedido detail returns typed response
- **WHEN** un admin envía GET /api/v1/admin/pedidos/{id}/
- **THEN** la respuesta sigue el schema `PedidoDetailResponse` con campos tipados

### Requirement: Pedido historial endpoint uses typed schema
El endpoint GET /api/v1/admin/pedidos/{id}/historial/ SHALL usar un `response_model` Pydantic tipado en lugar de construir una lista de dicts inline.

#### Scenario: Pedido historial returns typed response
- **WHEN** un admin envía GET /api/v1/admin/pedidos/{id}/historial/
- **THEN** la respuesta es una lista de `PedidoHistorialEntry` con campos tipados
