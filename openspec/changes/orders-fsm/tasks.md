## 1. Modelos SQLModel

- [x] 1.1 Crear `backend/app/modules/pedidos/model.py` con modelo `Pedido`: id, cliente_id (FK Usuario), estado_id (FK EstadoPedido), campos de snapshot de dirección (calle, ciudad, provincia, codigo_postal, referencia), total (DECIMAL(10,2)), costo_envio (DECIMAL(10,2) default 0), creado_en, actualizado_en
- [x] 1.2 Agregar modelo `DetallePedido` en el mismo archivo: id, pedido_id (FK Pedido), producto_id (FK Producto), cantidad (INTEGER > 0), precio_unitario (DECIMAL(10,2)), exclusiones (ARRAY(Integer) default [])
- [x] 1.3 Agregar modelo `HistorialEstadoPedido` en el mismo archivo: id, pedido_id (FK Pedido), estado_anterior_id (FK EstadoPedido nullable), estado_nuevo_id (FK EstadoPedido), actor_id (FK Usuario nullable), actor_tipo (Enum 'USUARIO'/'SISTEMA'), motivo (TEXT nullable), creado_en (no actualizable)

## 2. Migración Alembic

- [x] 2.1 Generar migración con `alembic revision --autogenerate -m "add pedidos module"` y verificar que incluye las tres tablas nuevas en orden correcto (Pedido → DetallePedido → HistorialEstadoPedido)
- [x] 2.2 Verificar que la migración es reversible (downgrade en orden inverso)

## 3. Schemas Pydantic v2

- [x] 3.1 Crear `backend/app/modules/pedidos/schemas.py` con `PedidoItemCreate` (producto_id, cantidad, exclusiones: list[int] = [])
- [x] 3.2 Agregar `PedidoCreate` (direccion_id: int, items: list[PedidoItemCreate])
- [x] 3.3 Agregar `DetallePedidoRead` (producto_id, cantidad, precio_unitario, exclusiones)
- [x] 3.4 Agregar `PedidoRead` (id, estado, direccion snapshot fields, items: list[DetallePedidoRead], total, costo_envio, creado_en)
- [x] 3.5 Agregar `EstadoTransicionCreate` (nuevo_estado: str, motivo: str | None = None) — motivo obligatorio cuando nuevo_estado == "CANCELADO"
- [x] 3.6 Agregar `HistorialEstadoRead` (id, estado_anterior, estado_nuevo, actor_id, actor_tipo, motivo, creado_en)

## 4. Repository

- [x] 4.1 Crear `backend/app/modules/pedidos/repository.py` con `PedidosRepository(BaseRepository[Pedido])`
- [x] 4.2 Implementar `get_by_id_with_items(pedido_id)` — eager load de DetallePedido y estado actual
- [x] 4.3 Implementar `get_historial(pedido_id)` — SELECT ordenado por creado_en ASC
- [x] 4.4 Agregar `DetallePedidoRepository(BaseRepository[DetallePedido])` — solo insert (no update/delete)
- [x] 4.5 Agregar `HistorialEstadoPedidoRepository(BaseRepository[HistorialEstadoPedido])` — solo insert (append-only, sin update/delete)

## 5. FSM Engine

- [x] 5.1 Crear `backend/app/modules/pedidos/fsm.py` con el dict `TRANSICIONES_VALIDAS: dict[str, list[str]]` según el mapa de estados definido en design.md
- [x] 5.2 Implementar función `validate_transition(estado_actual: str, estado_destino: str) -> None` — lanza `DomainException(422)` si la transición no es válida o si el estado destino es CONFIRMADO (reservado para webhook)
- [x] 5.3 Implementar función `check_cancel_permission(estado_actual: str, rol_actor: str) -> None` — lanza `DomainException(403)` si el rol no tiene permiso para cancelar desde ese estado (RN-FS08, RN-RB08)

## 6. Servicio

- [x] 6.1 Crear `backend/app/modules/pedidos/service.py` con clase `PedidosService`
- [x] 6.2 Implementar `crear_pedido(data: PedidoCreate, cliente: Usuario) -> PedidoRead` dentro de UoW: (a) validar que la dirección pertenece al cliente, (b) SELECT FOR UPDATE del stock de cada producto, (c) validar stock suficiente para todos los ítems antes de insertar cualuno, (d) insertar Pedido con snapshot de dirección y total calculado, (e) insertar DetallePedido por cada ítem con precio_unitario snapshot, (f) insertar HistorialEstadoPedido inicial (estado_anterior=NULL, estado_nuevo=PENDIENTE, actor_tipo=USUARIO)
- [x] 6.3 Implementar `get_pedido(pedido_id: int, actor: Usuario) -> PedidoRead` — verificar RBAC: Cliente solo ve pedidos propios (403 si no), Gestor/Admin ven cualquiera
- [x] 6.4 Implementar `transicionar_estado(pedido_id: int, data: EstadoTransicionCreate, actor: Usuario) -> PedidoRead` — (a) llamar validate_transition(), (b) si es CANCELADO llamar check_cancel_permission() y si viene de CONFIRMADO restaurar stock en UoW, (c) actualizar Pedido.estado_id, (d) insertar HistorialEstadoPedido con actor_id y actor_tipo=USUARIO
- [x] 6.5 Implementar `get_historial(pedido_id: int, actor: Usuario) -> list[HistorialEstadoRead]` — RBAC igual que get_pedido

## 7. Router

- [x] 7.1 Crear `backend/app/modules/pedidos/router.py` con prefijo `/api/v1/pedidos`
- [x] 7.2 Agregar `POST /` — llama `PedidosService.crear_pedido()`, requiere rol CLIENT (get_current_user)
- [x] 7.3 Agregar `GET /{pedido_id}` — llama `PedidosService.get_pedido()`, requiere autenticación
- [x] 7.4 Agregar `PATCH /{pedido_id}/estado` — llama `PedidosService.transicionar_estado()`, requiere autenticación; RBAC interno en servicio
- [x] 7.5 Agregar `GET /{pedido_id}/historial` — llama `PedidosService.get_historial()`, requiere autenticación

## 8. UoW y Registro

- [x] 8.1 Agregar `pedidos`, `detalle_pedidos` y `historial_estados` como atributos del `UnitOfWork` en `backend/app/core/uow.py`
- [x] 8.2 Registrar el router de pedidos en `backend/app/main.py`

## 9. Verificación Manual

- [ ] 9.1 Verificar POST /api/v1/pedidos crea pedido en PENDIENTE con snapshot correcto (precio y dirección)
- [ ] 9.2 Verificar que un pedido con stock insuficiente retorna 422 sin crear ningún registro
- [ ] 9.3 Verificar PATCH /{id}/estado con EN_PREP desde CONFIRMADO funciona para Gestor de Pedidos
- [ ] 9.4 Verificar PATCH /{id}/estado CANCELADO desde CONFIRMADO restaura el stock del producto
- [ ] 9.5 Verificar que PATCH con nuevo_estado=CONFIRMADO retorna 422 (reservado para webhook)
- [ ] 9.6 Verificar GET /{id}/historial retorna entradas en orden cronológico
- [ ] 9.7 Verificar que un Cliente no puede ver el pedido de otro usuario (403)
