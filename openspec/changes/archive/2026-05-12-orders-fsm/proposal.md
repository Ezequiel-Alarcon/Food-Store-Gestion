## Why

El catálogo, ingredientes, categorías y direcciones ya están operativos. El siguiente paso crítico es el núcleo de negocio: la creación de pedidos y la máquina de estados (FSM) que gobierna su ciclo de vida. Sin este change, nada puede generar revenue ni disparar pagos.

## What Changes

- Se agrega el módulo `pedidos/` en backend con modelos, repositorios, servicio y router.
- Se implementa creación de pedido atómica con Unit of Work: snapshots de precios (por ítem) y de dirección (en el pedido), validación de stock con SELECT FOR UPDATE.
- Se implementa la FSM de pedidos: motor de transiciones validadas + endpoints para avanzar estados manualmente.
- Se implementan las transiciones manuales: CONFIRMADO→EN_PREPARACION, EN_PREPARACION→EN_CAMINO, EN_CAMINO→ENTREGADO.
- Se implementa cancelación con restauración de stock (si venía de CONFIRMADO).
- Se implementa historial de estados append-only (HistorialEstadoPedido).
- **No incluido:** La transición PENDIENTE→CONFIRMADO y el decremento de stock al confirmar quedan reservados para `payments-integration` (se disparan vía webhook de MercadoPago).

## Capabilities

### New Capabilities

- `order-creation`: Creación de pedido atómica (POST /api/v1/pedidos) con snapshot de precios por ítem, snapshot de dirección en el pedido, validación de stock con SELECT FOR UPDATE dentro de la transacción UoW. Pedido nace en PENDIENTE con registro inicial en HistorialEstadoPedido.
- `order-transitions`: Motor FSM + endpoints de transición manual de estados (CONFIRMADO→EN_PREPARACION→EN_CAMINO→ENTREGADO), cancelación (desde PENDIENTE, CONFIRMADO, EN_PREPARACION con restricciones de rol) con restauración de stock atómica si venía de CONFIRMADO, y consulta del historial de estados append-only.

### Modified Capabilities

- `product-management`: El módulo de productos expone stock con SELECT FOR UPDATE durante creación/cancelación de pedidos. No cambia el contrato de la API pública, solo se documenta el uso concurrente del stock.

## Impact

- **Backend nuevo**: `backend/app/modules/pedidos/` — model.py, schemas.py, repository.py, service.py, router.py
- **Backend modificado**: `backend/app/main.py` (registro del router), `backend/app/modules/productos/` (uso del stock en contexto de pedidos)
- **Base de datos**: 3 tablas nuevas — `Pedido`, `DetallePedido`, `HistorialEstadoPedido`; las tablas `EstadoPedido` y `Producto.stock` ya existen desde `backend-config`
- **Dependencias**: `products-module` (FK Producto, stock), `addresses-module` (snapshot dirección), `auth-backend` (RBAC Gestor de Pedidos / Admin)
- **Sin cambios en frontend**: Este change es backend puro (Fase 2)
