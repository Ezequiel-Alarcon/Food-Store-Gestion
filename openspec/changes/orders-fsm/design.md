## Context

El módulo `pedidos/` no existe aún. Los módulos de productos (stock), direcciones (snapshots) y auth (RBAC) ya están operativos y archivados. Este change introduce el núcleo de negocio: el modelo de datos de pedidos, la operación de creación atómica, y la FSM que rige el ciclo de vida.

La transición PENDIENTE→CONFIRMADO y el decremento de stock al confirmar quedan fuera de este change (serán responsabilidad del webhook en `payments-integration`). La FSM debe estar diseñada para que `payments-integration` pueda invocarla sin modificar sus contratos.

## Goals / Non-Goals

**Goals:**
- Implementar modelos `Pedido`, `DetallePedido`, `HistorialEstadoPedido` con migración Alembic
- Creación de pedido atómica: validación de stock con SELECT FOR UPDATE, snapshot de precio por ítem, snapshot de dirección en el pedido
- Motor FSM en capa de servicio: validación de transiciones, registro append-only en historial
- Transiciones manuales: CONFIRMADO→EN_PREPARACION, EN_PREPARACION→EN_CAMINO, EN_CAMINO→ENTREGADO
- Cancelación desde PENDIENTE, CONFIRMADO (con restauración de stock), EN_PREPARACION (solo Admin)
- Endpoint de historial de estados por pedido (US-044)
- Endpoint de detalle de pedido por ID

**Non-Goals:**
- Transición PENDIENTE→CONFIRMADO (reservada para `payments-integration`)
- Decremento de stock en confirmación (idem)
- Listado de pedidos (reservado para `orders-list-gestor` y `orders-list-client`)
- Cualquier cambio de frontend

## Decisions

### 1. Snapshot inline en tablas de pedido (no tablas de snapshot separadas)

Los snapshots de dirección y precio se almacenan como campos planos en `Pedido` y `DetallePedido` respectivamente, sin FK vivas al modelo original.

```
Pedido
├── direccion_calle        TEXT (snapshot al momento de la compra)
├── direccion_ciudad       TEXT
├── direccion_provincia    TEXT
├── direccion_codigo_postal TEXT (nullable)
├── direccion_referencia   TEXT (nullable)

DetallePedido
├── precio_unitario        DECIMAL(10,2)  (snapshot del precio)
├── exclusiones            INTEGER[]      (IDs de ingredientes excluidos)
```

**Por qué no tablas separadas de snapshot**: Este proyecto no tiene un patrón de snapshot tables establecido. Los campos inline son más simples, requieren menos joins para reportes y ya están especificados en las HU (RN-PE02, RN-PE03, RN-DA06). Una tabla `DireccionSnapshot` sería over-engineering para este scope.

### 2. FSM como dict de transiciones en la capa de servicio

```python
TRANSICIONES_VALIDAS = {
    "PENDIENTE":      ["CANCELADO"],               # CONFIRMADO solo via webhook
    "CONFIRMADO":     ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["EN_CAMINO", "CANCELADO"],  # CANCELADO aquí solo Admin (RN-RB08)
    "EN_CAMINO":      ["ENTREGADO"],
    # ENTREGADO y CANCELADO: terminales (sin entradas)
}
```

El servicio valida la transición contra el dict antes de persistir. Si la transición no existe en el dict, retorna `DomainException(400)`. Si existe pero el rol no alcanza (ej. EN_PREPARACION→CANCELADO por no-Admin), retorna `DomainException(403)`.

**Por qué no un enum state machine library**: El proyecto no usa ninguna librería de FSM (statemachine, transitions). Agregar una dependencia para 5 estados y 7 transiciones es overkill. El dict es legible, testeable y coherente con el estilo del proyecto.

### 3. Un solo endpoint PATCH /api/v1/pedidos/{id}/estado para todas las transiciones manuales

```
PATCH /api/v1/pedidos/{id}/estado
Body: { "nuevo_estado": "EN_PREPARACION", "motivo": "optional" }
```

En vez de endpoints por transición (`/confirmar`, `/preparar`, `/despachar`, `/entregar`, `/cancelar`). El motor FSM en el servicio determina si la transición es válida según el estado actual.

**Por qué**: Menos endpoints para mantener, el cliente no necesita saber qué acción invocar — solo el estado destino. El estado actual se obtiene del pedido en DB, no del cliente.

### 4. HistorialEstadoPedido: actor_id + actor_tipo

```
HistorialEstadoPedido
├── pedido_id          FK Pedido
├── estado_anterior_id FK EstadoPedido (nullable para el estado inicial)
├── estado_nuevo_id    FK EstadoPedido
├── actor_id           FK Usuario (nullable — NULL cuando actor es SISTEMA)
├── actor_tipo         ENUM('USUARIO', 'SISTEMA')
├── motivo             TEXT (nullable, obligatorio en cancelaciones)
├── creado_en          TIMESTAMP (auto, no actualizable)
```

El campo `creado_en` es inmutable: la tabla es append-only (RN-DA05). El servicio nunca emite UPDATE ni DELETE sobre esta tabla.

### 5. Stock: validación en creación, restauración en cancelación desde CONFIRMADO

- **Creación**: `SELECT stock FROM productos WHERE id = ? FOR UPDATE` dentro de la UoW. Si `stock < cantidad_pedida` para cualquier ítem → rollback completo (RN-PE04, RN-PE05). El stock NO se decrementa en la creación.
- **PENDIENTE→CONFIRMADO** (payments-integration): Decrementa stock atómicamente.
- **Cancelación desde CONFIRMADO**: Restaura stock atómicamente con `UPDATE productos SET stock = stock + :cant`. Cancelación desde PENDIENTE no afecta stock (nunca se decrementó).

### 6. Endpoint de detalle de pedido

```
GET /api/v1/pedidos/{id}
```

Retorna el pedido con sus ítems y el último estado. El cliente solo puede ver sus propios pedidos (RN-RB05). Gestor de Pedidos y Admin pueden ver cualquiera.

## Risks / Trade-offs

- **Race condition en creación de múltiples pedidos simultáneos con mismo producto** → Mitigado con SELECT FOR UPDATE dentro de la transacción UoW. PostgreSQL bloquea la fila hasta el commit.
- **Cancelación de pedido CONFIRMADO con fallo en restauración de stock** → Mitigado: toda la operación va en un UoW; si falla el UPDATE de stock, hay rollback del cambio de estado. El pedido queda CONFIRMADO.
- **FSM acoplada al servicio** → Riesgo aceptable. Si el proyecto crece, el dict de transiciones puede extraerse a una clase `PedidoFSM`. En este scope es prematuro.
- **Snapshots de dirección desactualizados respecto al formato de la tabla `direcciones`** → Los campos del snapshot se copian en el momento de la creación. Cualquier cambio futuro en el modelo `Direccion` no afecta pedidos existentes (RN-DA06, intencional).

## Migration Plan

1. Alembic `revision --autogenerate`: genera migración para `pedidos`, `detalle_pedido`, `historial_estado_pedido`
2. Los valores de `estado_pedido` ya están en seed (`backend-config`): PENDIENTE(1), CONFIRMADO(2), EN_PREPARACION(3), EN_CAMINO(4), ENTREGADO(5), CANCELADO(6)
3. No hay datos existentes que migrar (tablas nuevas)
4. Rollback: `alembic downgrade -1` — DROP TABLE en orden inverso (historial → detalle → pedido)

## Open Questions

- ¿El `costo_envio` es fijo (ej. 0.00 por ahora) o configurable por dirección/sucursal? → Se asume `costo_envio = 0.00` hasta que `payments-integration` o `addresses-module` lo defina.
- ¿`Pedidos` necesita campo `observaciones` libre para el cliente? → No está en las HU, no se implementa.
