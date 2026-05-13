## ADDED Requirements

### Requirement: Admin can get general metrics
El sistema SHALL permitir a ADMIN y GESTOR obtener métricas generales del dashboard.

#### Scenario: Get general metrics as admin
- **WHEN** ADMIN envía GET /api/v1/admin/metrics/
- **THEN** el sistema devuelve {total_pedidos, pedidos_hoy, revenue_total, revenue_hoy, usuarios_activos, pedidos_pendientes}

#### Scenario: Get general metrics as gestor
- **WHEN** GESTOR envía GET /api/v1/admin/metrics/
- **THEN** el sistema devuelve las mismas métricas que para ADMIN

#### Scenario: Get general metrics as client
- **WHEN** CLIENT envía GET /api/v1/admin/metrics/
- **THEN** el sistema devuelve 403 Forbidden

### Requirement: Admin can get sales chart data
El sistema SHALL permitir a ADMIN y GESTOR obtener datos para gráfico de ventas de los últimos 30 días.

#### Scenario: Get sales chart as admin
- **WHEN** ADMIN envía GET /api/v1/admin/metrics/sales-chart/
- **THEN** el sistema devuelve array de {fecha, pedidos, revenue} para los últimos 30 días

#### Scenario: Get sales chart as gestor
- **WHEN** GESTOR envía GET /api/v1/admin/metrics/sales-chart/
- **THEN** el sistema devuelve el mismo array que para ADMIN

### Requirement: Admin can get top products
El sistema SHALL permitir a ADMIN y GESTOR obtener el top 10 productos más vendidos.

#### Scenario: Get top products as admin
- **WHEN** ADMIN envía GET /api/v1/admin/metrics/top-products/
- **THEN** el sistema devuelve array de {producto_id, nombre, unidades_vendidas, revenue} ordenado por unidades_vendidas desc, limit 10

#### Scenario: Get top products as gestor
- **WHEN** GESTOR envía GET /api/v1/admin/metrics/top-products/
- **THEN** el sistema devuelve el mismo array que para ADMIN

### Requirement: Admin can get orders by status
El sistema SHALL permitir a ADMIN y GESTOR obtener conteo de pedidos agrupados por estado.

#### Scenario: Get orders by status as admin
- **WHEN** ADMIN envía GET /api/v1/admin/metrics/orders-by-status/
- **THEN** el sistema devuelve array de {estado_codigo, nombre, cantidad} ordenado por cantidad desc

#### Scenario: Get orders by status as gestor
- **WHEN** GESTOR envía GET /api/v1/admin/metrics/orders-by-status/
- **THEN** el sistema devuelve el mismo array que para ADMIN