## Context

El módulo `admin/` está vacío (solo stubs de archivos). Change 17 `admin-metrics` lo completa con endpoints REST para métricas KPIs del dashboard. Acceso restringido a ADMIN y GESTOR.

## Goals / Non-Goals

**Goals:**
- Implementar 4 endpoints de métricas en `admin/router.py`
- Crear schemas de respuesta Pydantic v2 en `admin/schemas.py`
- Implementar lógica de queries agregadas en `admin/service.py`
- Tests de integración cubriendo los 4 endpoints

**Non-Goals:**
- No implementar frontend (Fase 3 — `admin-metrics-frontend`)
- No crear nuevos modelos — reutilizar `Pedido`, `Producto`, `Usuario` existentes
- No crear dashboard visual — solo endpoints JSON

## Decisions

### 1. Queries vs raw SQL

**Decision:** Usar SQLModel/SQLAlchemy queries en el service/repository en lugar de raw SQL.

**Rationale:** Sigue el patrón del proyecto (Router → Service → UoW → Repository → Model). SQLAlchemy 2.0 soporta aggregation functions (`func.count`, `func.sum`) nativamente.

**Alternatives considered:**
- Raw SQL con `text()` → No, viola el patrón del proyecto
- Vistas de BD (CREATE VIEW) → No, overkill para este scope

### 2. Métricas calculadas en queries vs aplicación

**Decision:** Calcular métricas directamente en PostgreSQL (queries agregadas).

**Rationale:** Más eficiente quetraer todos los pedidos y filtrar en Python. PostgreSQL optimiza queries de agregación con índices.

### 3. Dates — hardcoded vs parámetro

**Decision:** `sales-chart` hardcodea últimos 30 días; `top-products` sin límite temporal.

**Rationale:** Simplifica el scope. El frontend puede pasar parámetros de rango en future iterations si se necesita.

### 4. Permisos

**Decision:** ADMIN y GESTOR acceden a todas las métricas; CLIENT no tiene acceso.

**Rationale:** Consistente con `require_role("ADMIN", "GESTOR")` del pipeline auth existente.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Queries lentas con muchos pedidos | Crear índices compuestos en `pedidos.estado_codigo` + `pedidos.fecha_creacion` si no existen |
| Division by zero en revenue promedio | Retornar 0 si no hay pedidos completados |
| Datos faltantes (categorías sin productos) | Queries con LEFT JOIN para no perder categorías vacías |