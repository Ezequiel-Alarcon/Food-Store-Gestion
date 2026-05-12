## ADDED Requirements

### Requirement: FSM validates transitions against allowed map
El sistema SHALL validar toda transición de estado contra el mapa de transiciones válidas antes de persistir. Transiciones no definidas en el mapa son rechazadas con 422.

```
PENDIENTE      → [CANCELADO]
CONFIRMADO     → [EN_PREPARACION, CANCELADO]
EN_PREPARACION → [EN_CAMINO, CANCELADO]
EN_CAMINO      → [ENTREGADO]
ENTREGADO      → [] (terminal)
CANCELADO      → [] (terminal)
```

La transición PENDIENTE→CONFIRMADO está reservada para el webhook de pagos; no es accesible vía PATCH manual.

#### Scenario: Valid manual transition
- **WHEN** un usuario con rol PEDIDOS envía PATCH /api/v1/pedidos/{id}/estado con un estado destino válido para el estado actual
- **THEN** el sistema persiste el cambio, registra en historial y retorna 200 con el pedido actualizado

#### Scenario: Invalid transition attempt
- **WHEN** se intenta transicionar un pedido desde EN_CAMINO a EN_PREPARACION
- **THEN** el sistema retorna 422 indicando que la transición no es válida

#### Scenario: Transition from terminal state
- **WHEN** se intenta cambiar el estado de un pedido ENTREGADO o CANCELADO
- **THEN** el sistema retorna 422 indicando que el estado es terminal

#### Scenario: Manual attempt to set CONFIRMADO
- **WHEN** un usuario intenta PATCH /api/v1/pedidos/{id}/estado con nuevo_estado=CONFIRMADO
- **THEN** el sistema retorna 422; esa transición solo ocurre via webhook de pagos

### Requirement: CONFIRMADO to EN_PREPARACION transition
El sistema SHALL permitir a Gestor de Pedidos y Admin transicionar un pedido de CONFIRMADO a EN_PREPARACION.

#### Scenario: Gestor advances confirmed order to preparation
- **WHEN** un usuario con rol PEDIDOS envía PATCH con nuevo_estado=EN_PREPARACION sobre un pedido CONFIRMADO
- **THEN** el pedido pasa a EN_PREPARACION y se registra en historial con actor_id del usuario

#### Scenario: Cliente attempts to advance state
- **WHEN** un Cliente autenticado intenta PATCH /api/v1/pedidos/{id}/estado
- **THEN** el sistema retorna 403 Forbidden

### Requirement: EN_PREPARACION to EN_CAMINO transition
El sistema SHALL permitir a Gestor de Pedidos y Admin transicionar un pedido de EN_PREPARACION a EN_CAMINO.

#### Scenario: Gestor dispatches order
- **WHEN** un usuario con rol PEDIDOS envía PATCH con nuevo_estado=EN_CAMINO sobre un pedido EN_PREPARACION
- **THEN** el pedido pasa a EN_CAMINO y se registra en historial

### Requirement: EN_CAMINO to ENTREGADO transition
El sistema SHALL permitir a Gestor de Pedidos y Admin transicionar un pedido de EN_CAMINO a ENTREGADO. ENTREGADO es estado terminal.

#### Scenario: Gestor marks order as delivered
- **WHEN** un usuario con rol PEDIDOS envía PATCH con nuevo_estado=ENTREGADO sobre un pedido EN_CAMINO
- **THEN** el pedido pasa a ENTREGADO, se registra en historial y no puede cambiar de estado nuevamente

### Requirement: Cancel order with role-based restrictions
El sistema SHALL permitir cancelar pedidos según el estado y el rol del actor (RN-FS08):
- PENDIENTE: Cliente (propio), Gestor de Pedidos, Admin
- CONFIRMADO: Gestor de Pedidos, Admin
- EN_PREPARACION: solo Admin (RN-RB08)
- EN_CAMINO, ENTREGADO: nadie

#### Scenario: Client cancels own pending order
- **WHEN** un Cliente envía PATCH con nuevo_estado=CANCELADO sobre un pedido propio en PENDIENTE
- **THEN** el pedido pasa a CANCELADO; el stock no se modifica (nunca fue decrementado)

#### Scenario: Cancel confirmed order restores stock
- **WHEN** un usuario con rol PEDIDOS o ADMIN cancela un pedido en CONFIRMADO
- **THEN** el pedido pasa a CANCELADO y el stock de cada producto del pedido es restaurado atómicamente

#### Scenario: Gestor attempts to cancel order in EN_PREPARACION
- **WHEN** un usuario con rol PEDIDOS (sin ADMIN) intenta cancelar un pedido EN_PREPARACION
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Cancel with motivo required
- **WHEN** se cancela un pedido sin incluir el campo motivo
- **THEN** el sistema retorna 422; el campo motivo es obligatorio para cancelaciones

#### Scenario: Stock restoration is atomic on cancel
- **WHEN** falla la restauración del stock durante la cancelación de un pedido CONFIRMADO
- **THEN** el estado del pedido NO cambia a CANCELADO (rollback completo en UoW)

### Requirement: Append-only state history
El sistema SHALL registrar cada cambio de estado en HistorialEstadoPedido con: estado anterior, estado nuevo, timestamp, actor (usuario o SISTEMA), motivo (obligatorio en cancelaciones). Los registros son inmutables: nunca se actualizan ni eliminan (RN-DA05, RN-FS07, RN-FS09).

#### Scenario: History entry created on every transition
- **WHEN** un pedido cambia de estado (cualquier transición)
- **THEN** se inserta exactamente un nuevo registro en HistorialEstadoPedido

#### Scenario: History cannot be modified
- **WHEN** se intenta modificar o eliminar un registro del historial (vía cualquier endpoint)
- **THEN** no existe endpoint que permita tal operación; la capa de servicio no expone UPDATE/DELETE sobre historial

### Requirement: Query order state history
El sistema SHALL retornar el historial completo de estados de un pedido vía GET /api/v1/pedidos/{id}/historial en orden cronológico ascendente.

#### Scenario: Admin queries order history
- **WHEN** un Admin solicita GET /api/v1/pedidos/{id}/historial
- **THEN** retorna la lista cronológica de transiciones con estado anterior, estado nuevo, actor y timestamp

#### Scenario: Client queries own order history
- **WHEN** un Cliente solicita el historial de un pedido propio
- **THEN** el sistema retorna 200 con el historial completo del pedido

#### Scenario: Client queries another user's order history
- **WHEN** un Cliente solicita el historial de un pedido que no es suyo
- **THEN** el sistema retorna 403 Forbidden
