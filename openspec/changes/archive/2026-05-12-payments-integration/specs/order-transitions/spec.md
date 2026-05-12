## MODIFIED Requirements

### Requirement: FSM validates transitions against allowed map
El sistema SHALL validar toda transición de estado contra el mapa de transiciones válidas antes de persistir. Transiciones no definidas en el mapa son rechazadas con 422.

```
PENDIENTE      → [CONFIRMADO, CANCELADO]
CONFIRMADO     → [EN_PREP, CANCELADO]
EN_PREP        → [EN_CAMINO, CANCELADO]
EN_CAMINO      → [ENTREGADO]
ENTREGADO      → [] (terminal)
CANCELADO      → [] (terminal)
```

La transición PENDIENTE→CONFIRMADO es ejecutada exclusivamente por el SISTEMA en respuesta al webhook de pagos (`payment-webhook`). Ningún usuario puede ejecutarla manualmente.

#### Scenario: Valid manual transition
- **WHEN** un usuario con rol PEDIDOS envía PATCH /api/v1/pedidos/{id}/estado con un estado destino válido para el estado actual
- **THEN** el sistema persiste el cambio, registra en historial y retorna 200 con el pedido actualizado

#### Scenario: Invalid transition attempt
- **WHEN** se intenta transicionar un pedido desde EN_CAMINO a EN_PREP
- **THEN** el sistema retorna 422 indicando que la transición no es válida

#### Scenario: Transition from terminal state
- **WHEN** se intenta cambiar el estado de un pedido ENTREGADO o CANCELADO
- **THEN** el sistema retorna 422 indicando que el estado es terminal

#### Scenario: Manual attempt to set CONFIRMADO
- **WHEN** un usuario intenta PATCH /api/v1/pedidos/{id}/estado con nuevo_estado=CONFIRMADO
- **THEN** el sistema retorna 422; esa transición solo ocurre via webhook de pagos

#### Scenario: System confirms order via payment webhook
- **WHEN** el webhook de pagos recibe approved y el sistema ejecuta la transición PENDIENTE→CONFIRMADO
- **THEN** el pedido pasa a CONFIRMADO con actor=SISTEMA, se decrementa stock, y se registra en historial

### Requirement: Cancel order with role-based restrictions
El sistema SHALL permitir cancelar pedidos según el estado y el rol del actor (RN-FS08):
- PENDIENTE: Cliente (propio), Gestor de Pedidos, Admin
- CONFIRMADO: Gestor de Pedidos, Admin
- EN_PREP: solo Admin (RN-RB08)
- EN_CAMINO, ENTREGADO: nadie

#### Scenario: Client cancels own pending order
- **WHEN** un Cliente envía PATCH con nuevo_estado=CANCELADO sobre un pedido propio en PENDIENTE
- **THEN** el pedido pasa a CANCELADO; el stock no se modifica (nunca fue decrementado)

#### Scenario: Cancel confirmed order restores stock
- **WHEN** un usuario con rol PEDIDOS o ADMIN cancela un pedido en CONFIRMADO
- **THEN** el pedido pasa a CANCELADO y el stock de cada producto del pedido es restaurado atómicamente

#### Scenario: Gestor attempts to cancel order in EN_PREP
- **WHEN** un usuario con rol PEDIDOS (sin ADMIN) intenta cancelar un pedido EN_PREP
- **THEN** el sistema retorna 403 Forbidden

#### Scenario: Cancel with motivo required
- **WHEN** se cancela un pedido sin incluir el campo motivo
- **THEN** el sistema retorna 422; el campo motivo es obligatorio para cancelaciones

#### Scenario: Stock restoration is atomic on cancel
- **WHEN** falla la restauración del stock durante la cancelación de un pedido CONFIRMADO
- **THEN** el estado del pedido NO cambia a CANCELADO (rollback completo en UoW)
