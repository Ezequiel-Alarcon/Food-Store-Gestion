## 1. Schemas

- [x] 1.1 Completar `backend/app/modules/admin/schemas.py` con `GeneralMetricsResponse`, `SalesChartEntry`, `SalesChartResponse`, `TopProductEntry`, `OrdersByStatusEntry`
- [x] 1.2 Agregar `model_config = {"str_strip_whitespace": True}` en cada schema

## 2. Repository

- [x] 2.1 Completar `backend/app/modules/admin/repository.py` con queries agregadas: `get_general_metrics()`, `get_sales_chart(days)`, `get_top_products(limit)`, `get_orders_by_status()`
- [x] 2.2 Usar `func.count`, `func.sum`, `func.date_trunc` de SQLAlchemy para aggregations
- [x] 2.3 Seguir patrón `BaseRepository[Model]` existente

## 3. Service

- [x] 3.1 Completar `backend/app/modules/admin/service.py` con lógica de negocio
- [x] 3.2 Métodos: `get_general_metrics()`, `get_sales_chart()`, `get_top_products()`, `get_orders_by_status()`
- [x] 3.3 Manejar empty results (return defaults, no errors)

## 4. Router

- [x] 4.1 Completar `backend/app/modules/admin/router.py` con 4 endpoints:
  - GET /admin/metrics/ — general metrics
  - GET /admin/metrics/sales-chart/ — sales chart data
  - GET /admin/metrics/top-products/ — top products
  - GET /admin/metrics/orders-by-status/ — orders by status
- [x] 4.2 Proteger todos con require_role("ADMIN", "GESTOR")
- [x] 4.3 Agregar response_model en cada endpoint
- [x] 4.4 Registrar router en backend/app/main.py

## 5. Tests de Integración

- [x] 5.1 Crear directorio backend/tests/modules/admin/
- [x] 5.2 Crear backend/tests/modules/admin/__init__.py
- [x] 5.3 Crear backend/tests/modules/admin/test_admin_metrics.py
- [x] 5.4 Implementar test: test_general_metrics_admin_retorna_200
- [x] 5.5 Implementar test: test_general_metrics_gestor_retorna_200
- [x] 5.6 Implementar test: test_general_metrics_client_retorna_403
- [x] 5.7 Implementar test: test_sales_chart_admin_retorna_200
- [x] 5.8 Implementar test: test_top_products_admin_retorna_200
- [x] 5.9 Implementar test: test_orders_by_status_admin_retorna_200

## 6. Verificación

- [x] 6.1 Correr tests: pytest backend/tests/modules/admin/ -v
- [x] 6.2 Verificar que todos los tests pasen
- [x] 6.3 Verificar endpoints con auth (probar 200 con admin, 403 con client)