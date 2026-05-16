## Context

El módulo `admin` es un módulo transversal que consulta sobre modelos de otros dominios (`Pedido`, `Producto`, `Usuario`, etc.). Actualmente tiene 7 endpoints funcionales con 4 queries de agregación en `AdminRepository`, pero:
- `model.py` está vacío (solo un comentario)
- `AdminRepository` no hereda de `BaseRepository[T]` — es una clase standalone
- `AdminService` crea `SessionLocal()` directamente, bypassando UoW
- Endpoints de detalle de pedido construyen dicts inline sin schemas
- Queries no soportan filtros por fecha (HU US-056 a US-059 los piden)

## Goals / Non-Goals

**Goals:**
- Centralizar imports de modelos cruzados en `model.py`
- Alinear `AdminRepository` con el patrón `BaseRepository[T]` del proyecto
- Integrar Unit of Work en `AdminService`
- Agregar filtros temporales opcionales en queries de métricas
- Crear schemas para endpoints que usan dicts inline

**Non-Goals:**
- NO cambiar la firma de los endpoints existentes (backward compatible)
- NO migrar a vistas materializadas o tablas de resumen
- NO cambios en el frontend
- NO refactorizar la lógica de negocio de las métricas (solo agregar filtros)

## Decisions

### 1. model.py como módulo de re-exports
Admin no tiene entidades propias. Su `model.py` re-exporta los modelos de otros módulos que consulta: `Pedido`, `DetallePedido`, `Producto`, `Usuario`, `HistorialEstadoPedido`. Esto documenta explícitamente las dependencias cruzadas y centraliza imports.

**Alternativa considerada:** Dejar model.py vacío porque admin no tiene tablas propias. Se descarta porque el change explícitamente pide un model.py funcional y otros módulos usan model.py para documentar sus entidades.

### 2. AdminRepository NO hereda de BaseRepository
`AdminRepository` hace queries de agregación (COUNT, SUM, GROUP BY) que no encajan bien en el patrón CRUD genérico de `BaseRepository[T]`. Se mantiene como clase standalone pero se refactoriza para recibir `Session` de forma consistente (inyección desde el service/UoW).

**Alternativa considerada:** Crear un modelo dummy solo para heredar de BaseRepository. Se descarta porque es un hack innecesario — BaseRepository está diseñado para CRUD de una entidad, no para queries analíticas transversales.

### 3. Service usa UoW para lectura también
Aunque las queries de admin son solo lectura, se envuelven en `with uow:` para consistencia con el patrón del proyecto. El UoW abre y cierra la sesión correctamente incluso para reads.

### 4. Filtros de fecha son opcionales
Todos los nuevos parámetros `desde` y `hasta` son opcionales (`Optional[datetime] = None`). Sin filtros, el comportamiento es idéntico al actual (backward compatible).

### 5. Schemas para detalle de pedido
Se crean `PedidoDetailResponse` y `PedidoHistorialEntry` como schemas Pydantic v2. El router deja de construir dicts inline y usa `response_model` explícito.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Re-exports en model.py pueden crear import circular | Usar `TYPE_CHECKING` para imports de tipo, imports directos solo para SQLModel |
| AdminRepository sin BaseRepository pierde métodos genéricos | No necesita CRUD genérico — solo queries de agregación |
| Filtros de fecha requieren validación de formato | FastAPI parsea automáticamente datetime desde query params |
| Schemas nuevos para detalle de pedido pueden romper frontend si cambian campos | Se replica exactamente la estructura del dict inline actual |
