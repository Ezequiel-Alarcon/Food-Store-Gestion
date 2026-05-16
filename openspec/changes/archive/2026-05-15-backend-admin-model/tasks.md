## 1. Model.py — Re-exports centralizados

- [x] 1.1 Crear `model.py` con re-exports de `Pedido`, `DetallePedido`, `Producto`, `Usuario`, `HistorialEstadoPedido`

## 2. Repository — Agregar filtros temporales

- [x] 2.1 Agregar parámetros opcionales `desde` y `hasta` en `get_general_metrics()`
- [x] 2.2 Agregar parámetros opcionales `desde` y `hasta` en `get_sales_chart()` (reemplazar hardcode de 30 días)
- [x] 2.3 Agregar parámetros opcionales `desde` y `hasta` en `get_top_products()`
- [x] 2.4 Agregar parámetros opcionales `desde` y `hasta` en `get_orders_by_status()`
- [x] 2.5 Agregar método `get_total_usuarios_registrados()` — COUNT de todos los usuarios

## 3. Service — Integrar Unit of Work

- [x] 3.1 Refactorizar `AdminService.__init__` para recibir `UnitOfWork` o `Session` (no crear SessionLocal)
- [x] 3.2 Eliminar property `repo` que crea SessionLocal directamente
- [x] 3.3 Actualizar `get_general_metrics` para pasar filtros `desde`/`hasta` al repo
- [x] 3.4 Actualizar `get_sales_chart` para aceptar `desde`/`hasta` en lugar de `days`
- [x] 3.5 Actualizar `get_top_products` para pasar filtros `desde`/`hasta` al repo
- [x] 3.6 Actualizar `get_orders_by_status` para pasar filtros `desde`/`hasta` al repo
- [x] 3.7 Agregar método `get_total_usuarios_registrados()` en service

## 4. Router — Query params y schemas tipados

- [x] 4.1 Agregar query params `desde` y `hasta` en endpoint GET /admin/metrics/sales-chart/
- [x] 4.2 Agregar query params `desde` y `hasta` en endpoint GET /admin/metrics/top-products/
- [x] 4.3 Agregar query params `desde` y `hasta` en endpoint GET /admin/metrics/orders-by-status/
- [x] 4.4 Crear schema `PedidoDetailResponse` para detalle de pedido
- [x] 4.5 Crear schema `PedidoHistorialEntry` para historial de estados
- [x] 4.6 Reemplazar dict inline en GET /admin/pedidos/{id}/ por `response_model=PedidoDetailResponse`
- [x] 4.7 Reemplazar list[dict] inline en GET /admin/pedidos/{id}/historial/ por `response_model=list[PedidoHistorialEntry]`

## 5. Schemas — Actualizar GeneralMetricsResponse

- [x] 5.1 Agregar campo `total_usuarios` en `GeneralMetricsResponse`

## 6. Tests

- [x] 6.1 Crear `test_repository.py` — tests unitarios para AdminRepository con filtros de fecha
- [x] 6.2 Crear `test_service.py` — tests unitarios para AdminService con UoW mockeado
- [x] 6.3 Crear `test_admin_filters.py` — tests de integración para endpoints con filtros de fecha
- [x] 6.4 Crear tests para schemas `PedidoDetailResponse` y `PedidoHistorialEntry`
