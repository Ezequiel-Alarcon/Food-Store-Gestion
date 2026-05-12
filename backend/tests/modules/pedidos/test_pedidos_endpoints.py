"""
Tests de integración para el módulo de pedidos.

Verifica los 7 escenarios de la sección 9 (Verificación Manual) del change orders-fsm:
  9.1 POST / crea pedido en PENDIENTE con snapshot correcto
  9.2 Stock insuficiente retorna 422 sin crear registros
  9.3 PATCH estado EN_PREP desde CONFIRMADO para Gestor de Pedidos
  9.4 PATCH CANCELADO desde CONFIRMADO restaura stock
  9.5 PATCH con CONFIRMADO retorna 422 (webhook-only)
  9.6 GET historial en orden cronológico
  9.7 Cliente no puede ver pedido de otro usuario (403)
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select


# ── Helpers ──────────────────────────────────────────────────────────

def _decode_jwt_sub(token: str) -> int:
    """Extrae el user_id (sub) de un JWT sin verificarlo contra DB."""
    import base64, json
    # JWT: header.payload.signature
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token inválido")
    # Decodificar payload (base64url)
    payload_b64 = parts[1]
    # Agregar padding
    payload_b64 += "=" * (4 - len(payload_b64) % 4)
    payload_bytes = base64.urlsafe_b64decode(payload_b64)
    payload = json.loads(payload_bytes)
    return int(payload["sub"])


def _register_and_login(client: TestClient, email: str, password: str = "Password1", nombre: str = "Test") -> dict:
    """Registra un usuario CLIENT y devuelve tokens + user_id extraído del JWT."""
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "nombre": nombre},
    )
    assert resp.status_code == 201, f"Register failed: {resp.json()}"
    tokens = resp.json()
    user_id = _decode_jwt_sub(tokens["access_token"])
    return {
        "user_id": user_id,
        "email": email,
        "access_token": tokens["access_token"],
    }


def _create_address(session: Session, user_id: int) -> int:
    """Crea una dirección de prueba directamente en DB y devuelve su ID."""
    from app.modules.direcciones.model import UserAddress

    addr = UserAddress(
        user_id=user_id,
        calle="Av. Corrientes",
        numero="1234",
        ciudad="CABA",
        provincia="Buenos Aires",
        codigo_postal="C1043AAZ",
        pais="Argentina",
        referencias="Entre Callao y Riobamba",
        is_default=True,
        activa=True,
    )
    session.add(addr)
    session.flush()
    return addr.id


def _create_product(session: Session, nombre: str, precio: float, stock: int = 10, activo: bool = True) -> int:
    """Crea un producto directamente en DB y devuelve su ID."""
    from app.modules.productos.model import Producto

    prod = Producto(
        nombre=nombre,
        precio=precio,
        stock=stock,
        activo=activo,
    )
    session.add(prod)
    session.flush()
    return prod.id


def _seed_estados(session: Session) -> None:
    """Inserta los 6 estados de pedido en DB."""
    from app.modules.pedidos.model import EstadoPedido

    estados = [
        ("PENDIENTE", "Pendiente", 1, False),
        ("CONFIRMADO", "Confirmado", 2, False),
        ("EN_PREP", "En Preparación", 3, False),
        ("EN_CAMINO", "En Camino", 4, False),
        ("ENTREGADO", "Entregado", 5, True),
        ("CANCELADO", "Cancelado", 6, True),
    ]
    for codigo, nombre, orden, terminal in estados:
        existing = session.get(EstadoPedido, codigo)
        if not existing:
            session.add(EstadoPedido(codigo=codigo, nombre=nombre, orden=orden, es_terminal=terminal))
    session.flush()


def _force_estado_pedido(session: Session, pedido_id: int, nuevo_codigo: str) -> None:
    """Fuerza el estado de un pedido directamente (simula webhook de pago)."""
    from app.modules.pedidos.model import Pedido

    pedido = session.get(Pedido, pedido_id)
    if pedido:
        pedido.estado_codigo = nuevo_codigo
        session.add(pedido)
        session.flush()


# ── Cliente autenticado helper ───────────────────────────────────────

class AuthClient:
    """Wraps TestClient con token JWT para requests autenticados."""

    def __init__(self, client: TestClient, access_token: str):
        self._client = client
        self._token = access_token

    def post(self, url: str, json: dict | None = None):
        headers = {"Authorization": f"Bearer {self._token}"}
        return self._client.post(url, json=json, headers=headers)

    def get(self, url: str):
        headers = {"Authorization": f"Bearer {self._token}"}
        return self._client.get(url, headers=headers)

    def patch(self, url: str, json: dict | None = None):
        headers = {"Authorization": f"Bearer {self._token}"}
        return self._client.patch(url, json=json, headers=headers)


# ── Fixture de setup ─────────────────────────────────────────────────

@pytest.fixture(name="setup")
def fixture_setup(client, session):
    """Prepara la DB con estados, productos y un usuario CLIENT listo."""
    _seed_estados(session)

    # Productos de prueba
    prod_a = _create_product(session, "Hamburguesa Test", 1200.0, stock=50)
    prod_b = _create_product(session, "Papas Fritas Test", 600.0, stock=100)
    prod_stock_bajo = _create_product(session, "Producto Escaso", 500.0, stock=1)

    # Registrar CLIENT
    user_data = _register_and_login(client, "cliente_test@test.com")
    user_id = user_data["user_id"]
    access_token = user_data["access_token"]

    # Crear dirección para el CLIENT
    addr_id = _create_address(session, user_id)

    return {
        "client": client,
        "session": session,
        "user_id": user_id,
        "access_token": access_token,
        "addr_id": addr_id,
        "prod_a": prod_a,
        "prod_b": prod_b,
        "prod_stock_bajo": prod_stock_bajo,
    }


# ── 9.1 Crear pedido en PENDIENTE con snapshot correcto ──────────────

def test_crear_pedido_pendiente_snapshot(setup):
    """9.1: POST / crea pedido en PENDIENTE con snapshot correcto (precio y dirección)."""
    ac = AuthClient(setup["client"], setup["access_token"])

    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [
            {"producto_id": setup["prod_a"], "cantidad": 2},
            {"producto_id": setup["prod_b"], "cantidad": 1},
        ],
    })

    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.json()}"
    data = resp.json()

    # Estado inicial
    assert data["estado_codigo"] == "PENDIENTE"

    # Snapshot de dirección
    assert data["direccion_calle"] == "Av. Corrientes"
    assert data["direccion_numero"] == "1234"
    assert data["direccion_ciudad"] == "CABA"
    assert data["direccion_pais"] == "Argentina"

    # Total calculado: (2 × 1200) + (1 × 600) = 3000
    assert data["total"] == 3000.0
    assert data["costo_envio"] == 0.0

    # Items con precio snapshot
    assert len(data["items"]) == 2
    items_por_producto = {it["producto_id"]: it for it in data["items"]}
    assert items_por_producto[setup["prod_a"]]["precio_unitario"] == 1200.0
    assert items_por_producto[setup["prod_a"]]["cantidad"] == 2
    assert items_por_producto[setup["prod_b"]]["precio_unitario"] == 600.0
    assert items_por_producto[setup["prod_b"]]["cantidad"] == 1

    # Cliente asignado
    assert data["cliente_id"] == setup["user_id"]


# ── 9.2 Stock insuficiente retorna 422 sin crear registros ───────────

def test_stock_insuficiente_422_sin_registros(setup):
    """9.2: Pedir más de lo que hay en stock retorna 422 y NO crea ningún registro."""
    ac = AuthClient(setup["client"], setup["access_token"])

    # Producto escaso tiene stock=1, pedimos 5
    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [
            {"producto_id": setup["prod_stock_bajo"], "cantidad": 5},
        ],
    })

    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}: {resp.json()}"
    error_data = resp.json()
    assert "Stock insuficiente" in error_data["detail"]

    # Verificar que NO se creó ningún pedido en la DB
    from app.modules.pedidos.model import Pedido, DetallePedido, HistorialEstadoPedido
    pedidos = setup["session"].exec(select(Pedido)).all()
    detalles = setup["session"].exec(select(DetallePedido)).all()
    historial = setup["session"].exec(select(HistorialEstadoPedido)).all()
    assert len(pedidos) == 0, f"Se crearon {len(pedidos)} pedidos cuando no debía crearse ninguno"
    assert len(detalles) == 0
    assert len(historial) == 0

    # Verificar que el stock NO fue modificado
    from app.modules.productos.model import Producto
    prod = setup["session"].get(Producto, setup["prod_stock_bajo"])
    assert prod.stock == 1, f"El stock fue modificado: ahora es {prod.stock}"


# ── 9.3 PATCH EN_PREP desde CONFIRMADO (Gestor de Pedidos) ──────────

def test_transicion_en_prep_desde_confirmado(setup):
    """9.3: PATCH estado EN_PREP desde CONFIRMADO funciona para ADMIN."""
    ac = AuthClient(setup["client"], setup["access_token"])

    # Crear pedido (queda en PENDIENTE)
    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 1}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # Forzar transición a CONFIRMADO (simula webhook de pago) directo en DB
    _force_estado_pedido(setup["session"], pedido_id, "CONFIRMADO")

    # Registrar usuario ADMIN para transicionar
    admin_data = _register_and_login(setup["client"], "admin_test@test.com")
    # Necesitamos cambiar el rol a ADMIN manualmente
    from app.modules.auth.model import Usuario
    admin_user = setup["session"].get(Usuario, admin_data["user_id"])
    admin_user.rol = "ADMIN"
    setup["session"].add(admin_user)
    setup["session"].flush()

    admin_ac = AuthClient(setup["client"], admin_data["access_token"])

    # Transicionar a EN_PREP
    resp2 = admin_ac.patch(f"/api/v1/pedidos/{pedido_id}/estado", json={
        "nuevo_estado": "EN_PREP",
    })

    assert resp2.status_code == 200, f"Expected 200, got {resp2.status_code}: {resp2.json()}"
    assert resp2.json()["estado_codigo"] == "EN_PREP"


# ── 9.4 PATCH CANCELADO desde CONFIRMADO restaura stock ──────────────

def test_cancelar_desde_confirmado_restaura_stock(setup):
    """9.4: CANCELADO desde CONFIRMADO restaura el stock del producto."""
    ac = AuthClient(setup["client"], setup["access_token"])

    # Producto de prueba con stock conocido
    stock_inicial = setup["session"].get(
        __import__("app.modules.productos.model", fromlist=["Producto"]).Producto,
        setup["prod_a"],
    ).stock

    # Crear pedido con 3 unidades del producto A
    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 3}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # NOTA: En el servicio actual, NO se descuenta stock al crear el pedido
    # (solo se valida). El descuento ocurriría en el webhook de pago.
    # Verificar que el stock NO cambió al crear
    from app.modules.productos.model import Producto
    prod = setup["session"].get(Producto, setup["prod_a"])
    stock_despues_crear = prod.stock
    assert stock_despues_crear == stock_inicial, "El stock no debe cambiar al crear pedido"

    # Forzar CONFIRMADO (simula pago aprobado)
    _force_estado_pedido(setup["session"], pedido_id, "CONFIRMADO")

    # Simular que el stock fue descontado en el webhook de pago
    prod.stock = stock_inicial - 3
    setup["session"].add(prod)
    setup["session"].flush()

    # Admin cancela desde CONFIRMADO
    admin_data = _register_and_login(setup["client"], "admin_cancel@test.com")
    from app.modules.auth.model import Usuario
    admin_user = setup["session"].get(Usuario, admin_data["user_id"])
    admin_user.rol = "ADMIN"
    setup["session"].add(admin_user)
    setup["session"].flush()

    admin_ac = AuthClient(setup["client"], admin_data["access_token"])

    resp2 = admin_ac.patch(f"/api/v1/pedidos/{pedido_id}/estado", json={
        "nuevo_estado": "CANCELADO",
        "motivo": "Cliente se arrepintió",
    })

    assert resp2.status_code == 200, f"Expected 200, got {resp2.status_code}: {resp2.json()}"
    assert resp2.json()["estado_codigo"] == "CANCELADO"

    # Verificar que el stock fue RESTAURADO
    setup["session"].expire_all()
    prod = setup["session"].get(Producto, setup["prod_a"])
    assert prod.stock == stock_inicial, (
        f"Stock no restaurado: era {stock_inicial - 3} después del descuento simulado, "
        f"pero después de cancelar es {prod.stock}"
    )


# ── 9.5 PATCH CONFIRMADO manual retorna 422 ─────────────────────────

def test_confirmado_manual_422(setup):
    """9.5: PATCH con nuevo_estado=CONFIRMADO retorna 422 (reservado para webhook)."""
    ac = AuthClient(setup["client"], setup["access_token"])

    # Crear pedido en PENDIENTE
    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 1}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # Intentar transicionar manualmente a CONFIRMADO
    resp2 = ac.patch(f"/api/v1/pedidos/{pedido_id}/estado", json={
        "nuevo_estado": "CONFIRMADO",
    })

    assert resp2.status_code == 422, f"Expected 422, got {resp2.status_code}: {resp2.json()}"
    assert "exclusiva del webhook" in resp2.json()["detail"].lower() or \
           "CONFIRMADO" in resp2.json()["detail"]

    # Verificar que el pedido sigue en PENDIENTE
    resp3 = ac.get(f"/api/v1/pedidos/{pedido_id}")
    assert resp3.json()["estado_codigo"] == "PENDIENTE"


# ── 9.6 GET historial en orden cronológico ───────────────────────────

def test_historial_orden_cronologico(setup):
    """9.6: GET /{id}/historial retorna entradas en orden cronológico."""
    ac = AuthClient(setup["client"], setup["access_token"])

    # Crear admin para transiciones
    admin_data = _register_and_login(setup["client"], "admin_hist@test.com")
    from app.modules.auth.model import Usuario
    admin_user = setup["session"].get(Usuario, admin_data["user_id"])
    admin_user.rol = "ADMIN"
    setup["session"].add(admin_user)
    setup["session"].flush()
    admin_ac = AuthClient(setup["client"], admin_data["access_token"])

    # Crear pedido (genera entrada inicial PENDIENTE)
    resp = ac.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 1}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # Forzar CONFIRMADO en DB (simula webhook)
    _force_estado_pedido(setup["session"], pedido_id, "CONFIRMADO")

    # Transicionar a EN_PREP
    admin_ac.patch(f"/api/v1/pedidos/{pedido_id}/estado", json={"nuevo_estado": "EN_PREP"})

    # Obtener historial
    resp_hist = ac.get(f"/api/v1/pedidos/{pedido_id}/historial")
    assert resp_hist.status_code == 200, f"Expected 200, got {resp_hist.status_code}"
    historial = resp_hist.json()

    assert len(historial) >= 2, f"Expected at least 2 entries, got {len(historial)}"

    # Verificar orden cronológico: PENDIENTE → CONFIRMADO → EN_PREP
    estados_en_orden = [h["estado_nuevo_codigo"] for h in historial]
    assert estados_en_orden[0] == "PENDIENTE", f"First should be PENDIENTE, got {estados_en_orden}"
    # Nota: CONFIRMADO se forzó en DB (no por FSM), no genera entrada en historial
    # Así que el orden debería ser: PENDIENTE (registro inicial) → EN_PREP (por admin)
    # Pero el test solo verifica que haya orden cronológico (creado_en ASC)
    timestamps = [h["creado_en"] for h in historial]
    assert timestamps == sorted(timestamps), "El historial no está en orden cronológico"


# ── 9.7 Cliente no puede ver pedido de otro usuario (403) ────────────

def test_cliente_no_puede_ver_pedido_ajeno(setup):
    """9.7: Cliente no puede ver el pedido de otro usuario (403)."""
    ac1 = AuthClient(setup["client"], setup["access_token"])

    # Crear pedido para el CLIENT 1
    resp = ac1.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 1}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # Registrar otro CLIENT
    user2 = _register_and_login(setup["client"], "otro_cliente@test.com")
    ac2 = AuthClient(setup["client"], user2["access_token"])

    # CLIENT 2 intenta ver el pedido de CLIENT 1
    resp2 = ac2.get(f"/api/v1/pedidos/{pedido_id}")

    assert resp2.status_code == 403, (
        f"Expected 403 for cross-user access, got {resp2.status_code}: {resp2.json()}"
    )
    assert "acceso" in resp2.json()["detail"].lower() or \
           "No tenés" in resp2.json()["detail"]


def test_cliente_no_puede_ver_historial_ajeno(setup):
    """9.7 (extensión): Cliente no puede ver el historial de pedido ajeno."""
    ac1 = AuthClient(setup["client"], setup["access_token"])

    # Crear pedido
    resp = ac1.post("/api/v1/pedidos/", json={
        "direccion_id": setup["addr_id"],
        "items": [{"producto_id": setup["prod_a"], "cantidad": 1}],
    })
    assert resp.status_code == 201
    pedido_id = resp.json()["id"]

    # Otro CLIENT intenta ver el historial
    user2 = _register_and_login(setup["client"], "tercer_cliente@test.com")
    ac2 = AuthClient(setup["client"], user2["access_token"])

    resp2 = ac2.get(f"/api/v1/pedidos/{pedido_id}/historial")

    assert resp2.status_code == 403, (
        f"Expected 403 for cross-user historial, got {resp2.status_code}: {resp2.json()}"
    )
