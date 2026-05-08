"""
Seed data - Datos iniciales obligatorios para el sistema.
Ejecutar DESPUÉS de alembic upgrade head.

Los imports son condicionales: si un modelo aún no está implementado
(el proyecto está en desarrollo), esa parte del seed se omite.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from app.core.database import SessionLocal
from app.core.security import hash_password

# ── Imports condicionales (modelos pueden no existir aún en desarrollo) ──

try:
    from app.modules.auth.model import Rol, Usuario, UsuarioRol
except ImportError:
    Rol = None          # type: ignore
    Usuario = None      # type: ignore
    UsuarioRol = None   # type: ignore

try:
    from app.modules.pedidos.model import EstadoPedido
except ImportError:
    EstadoPedido = None  # type: ignore

try:
    from app.modules.pagos.model import FormaPago
except ImportError:
    FormaPago = None     # type: ignore


def run_seed() -> None:
    """
    Ejecuta el seed de datos iniciales.
    Debe llamarse DESPUÉS de alembic upgrade head.
    """
    with SessionLocal() as session:
        # Seed de Roles
        seed_roles(session)

        # Seed de Estados de Pedido
        seed_estados_pedido(session)

        # Seed de Formas de Pago
        seed_formas_pago(session)

        # Seed de Usuario Admin
        seed_usuario_admin(session)

        session.commit()
        print("✓ Seed completado exitosamente")


def seed_roles(session: Session) -> None:
    """Inserta los 4 roles del sistema RBAC."""
    if Rol is None:
        print("  ⚠ Seed roles omitido — modelo Rol no disponible aún")
        return

    roles_data = [
        {"codigo": "ADMIN", "nombre": "Administrador", "descripcion": "Acceso total al sistema"},
        {"codigo": "STOCK", "nombre": "Gestor de Stock", "descripcion": "Gestión de inventario y catálogo"},
        {"codigo": "PEDIDOS", "nombre": "Gestor de Pedidos", "descripcion": "Gestión de pedidos y estados"},
        {"codigo": "CLIENT", "nombre": "Cliente", "descripcion": "Usuario final del sistema"},
    ]

    for role_data in roles_data:
        existing = session.get(Rol, role_data["codigo"])
        if not existing:
            rol = Rol(**role_data)
            session.add(rol)
            print(f"  ✓ Rol creado: {role_data['codigo']}")
        else:
            print(f"  - Rol ya existe: {role_data['codigo']}")


def seed_estados_pedido(session: Session) -> None:
    """Inserta los 6 estados de la máquina de estados del pedido."""
    if EstadoPedido is None:
        print("  ⚠ Seed estados omitido — modelo EstadoPedido no disponible aún")
        return

    estados_data = [
        {"codigo": "PENDIENTE", "nombre": "Pendiente", "descripcion": "Pedido creado, esperando pago", "orden": 1, "es_terminal": False},
        {"codigo": "CONFIRMADO", "nombre": "Confirmado", "descripcion": "Pago aprobado", "orden": 2, "es_terminal": False},
        {"codigo": "EN_PREP", "nombre": "En Preparación", "descripcion": "En cocina", "orden": 3, "es_terminal": False},
        {"codigo": "EN_CAMINO", "nombre": "En Camino", "descripcion": "Despachado al cliente", "orden": 4, "es_terminal": False},
        {"codigo": "ENTREGADO", "nombre": "Entregado", "descripcion": "Entrega confirmada", "orden": 5, "es_terminal": True},
        {"codigo": "CANCELADO", "nombre": "Cancelado", "descripcion": "Pedido cancelado", "orden": 6, "es_terminal": True},
    ]

    for estado_data in estados_data:
        existing = session.get(EstadoPedido, estado_data["codigo"])
        if not existing:
            estado = EstadoPedido(**estado_data)
            session.add(estado)
            print(f"  ✓ Estado creado: {estado_data['codigo']}")
        else:
            print(f"  - Estado ya existe: {estado_data['codigo']}")


def seed_formas_pago(session: Session) -> None:
    """Inserta las 3 formas de pago."""
    if FormaPago is None:
        print("  ⚠ Seed formas de pago omitido — modelo FormaPago no disponible aún")
        return

    formas_data = [
        {"codigo": "MERCADOPAGO", "nombre": "MercadoPago", "descripcion": "Pago con MercadoPago", "habilitado": True},
        {"codigo": "EFECTIVO", "nombre": "Efectivo", "descripcion": "Pago en efectivo al recibir", "habilitado": True},
        {"codigo": "TRANSFERENCIA", "nombre": "Transferencia", "descripcion": "Transferencia bancaria", "habilitado": True},
    ]

    for forma_data in formas_data:
        existing = session.get(FormaPago, forma_data["codigo"])
        if not existing:
            forma = FormaPago(**forma_data)
            session.add(forma)
            print(f"  ✓ Forma de pago creada: {forma_data['codigo']}")
        else:
            print(f"  - Forma de pago ya existe: {forma_data['codigo']}")


def seed_usuario_admin(session: Session) -> None:
    """Crea el usuario administrador inicial."""
    if Usuario is None or UsuarioRol is None:
        print("  ⚠ Seed admin omitido — modelos Usuario/UsuarioRol no disponibles aún")
        return

    admin_email = "admin@foodstore.com"
    admin_password = "Admin1234!"

    # Verificar si ya existe
    statement = select(Usuario).where(Usuario.email == admin_email)
    existing = session.exec(statement).first()

    if existing:
        print(f"  - Usuario admin ya existe: {admin_email}")
        return

    # Crear usuario admin
    usuario = Usuario(
        nombre="Admin",
        apellido="Admin",
        email=admin_email,
        password_hash=hash_password(admin_password),
        telefono="+5491112345678",
        creado_en=datetime.now(timezone.utc),
        actualizado_en=datetime.now(timezone.utc),
    )
    session.add(usuario)
    session.flush()  # Obtener el ID

    # Asignar rol ADMIN
    usuario_rol = UsuarioRol(
        usuario_id=usuario.id,
        rol_codigo="ADMIN",
    )
    session.add(usuario_rol)

    print(f"  ✓ Usuario admin creado: {admin_email}")
    print(f"  ✓ Contraseña: {admin_password}")


if __name__ == "__main__":
    print("Iniciando seed de datos...")
    run_seed()
