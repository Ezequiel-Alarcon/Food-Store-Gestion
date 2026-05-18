"""
Seed data - Datos iniciales obligatorios para el sistema.
Ejecutar DESPUÉS de alembic upgrade head.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from app.core.database import SessionLocal
from app.core.security import hash_password

# ── Imports de modelos ──
from app.modules.auth.model import Usuario

try:
    from app.modules.pedidos.model import EstadoPedido
except ImportError:
    EstadoPedido = None  # type: ignore

try:
    from app.modules.productos.model import Producto, ProductoCategoria, ProductoIngrediente
except ImportError:
    Producto = None      # type: ignore
    ProductoCategoria = None   # type: ignore
    ProductoIngrediente = None    # type: ignore


def run_seed() -> None:
    """
    Ejecuta el seed de datos iniciales.
    Debe llamarse DESPUÉS de alembic upgrade head.
    """
    with SessionLocal() as session:
        # Documentar los 4 roles del sistema
        seed_roles(session)

        # Seed de Estados de Pedido
        seed_estados_pedido(session)

        # Seed de Usuario Admin
        seed_usuario_admin(session)

        # Seed de Productos
        seed_productos(session)

        session.commit()
        print("✓ Seed completado exitosamente")


def seed_roles(session: Session) -> None:
    """Documenta los 4 roles del sistema RBAC (almacenados como string en Usuario.rol)."""
    roles = [
        ("ADMIN", "Administrador — acceso total al sistema"),
        ("STOCK", "Gestor de Stock — gestión de inventario y catálogo"),
        ("PEDIDOS", "Gestor de Pedidos — gestión de pedidos y estados"),
        ("CLIENT", "Cliente — usuario final del sistema"),
    ]
    print("  ℹ Roles del sistema RBAC (almacenados en Usuario.rol):")
    for codigo, desc in roles:
        print(f"    • {codigo}: {desc}")


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


def seed_usuario_admin(session: Session) -> None:
    """Crea el usuario administrador inicial."""
    admin_email = "admin@foodstore.com"
    admin_password = "Admin1234!"

    # Verificar si ya existe
    statement = select(Usuario).where(Usuario.email == admin_email)
    existing = session.exec(statement).first()

    if existing:
        print(f"  - Usuario admin ya existe: {admin_email}")
        return

    # Crear usuario admin con los campos reales del modelo
    usuario = Usuario(
        nombre="Admin",
        apellido="Sistema",
        email=admin_email,
        password_hash=hash_password(admin_password),
        rol="ADMIN",
        telefono="+5491112345678",
        activo=True,
    )
    session.add(usuario)
    session.flush()

    print(f"  ✓ Usuario admin creado: {admin_email}")
    print(f"  ✓ Contraseña: {admin_password}")


def seed_productos(session: Session) -> None:
    """Inserta productos de ejemplo en el catálogo."""
    if Producto is None:
        print("  ⚠ Seed productos omitido — modelo Producto no disponible aún")
        return

    # Verificar si ya hay productos
    statement = select(Producto)
    existing = session.exec(statement).first()
    if existing:
        print("  - Productos ya existen en el catálogo")
        return

    # Productos de ejemplo
    productos_data = [
        {
            "nombre": "Hamburguesa Clásica",
            "descripcion": "Hamburguesa con queso, lechuga, tomate y salsa especial",
            "precio": 1200.00,
            "imagen_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
            "stock": 50,
            "activo": True,
            "categoria_nombre": "Hamburguesas",
            "ingrediente_nombres": ["Carne de res", "Pan", "Queso", "Lechuga", "Tomate"],
        },
        {
            "nombre": "Hamburguesa BBQ",
            "descripcion": "Hamburguesa con cebolla caramelizada, bacon y salsa barbacoa",
            "precio": 1450.00,
            "imagen_url": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400",
            "stock": 30,
            "activo": True,
            "categoria_nombre": "Hamburguesas",
            "ingrediente_nombres": ["Carne de res", "Pan", "Bacon", "Cebolla", "Salsa BBQ"],
        },
        {
            "nombre": "Pizza Margarita",
            "descripcion": "Pizza clásica con tomate, mozzarella y albahaca",
            "precio": 1800.00,
            "imagen_url": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=400",
            "stock": 25,
            "activo": True,
            "categoria_nombre": "Pizzas",
            "ingrediente_nombres": ["Masa", "Tomate", "Mozzarella", "Albahaca", "Aceite de oliva"],
        },
        {
            "nombre": "Pizza Napolitana",
            "descripcion": "Pizza con salsa de tomate, mozzarella y jamón",
            "precio": 1950.00,
            "imagen_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400",
            "stock": 20,
            "activo": True,
            "categoria_nombre": "Pizzas",
            "ingrediente_nombres": ["Masa", "Tomate", "Mozzarella", "Jamón", "Oregano"],
        },
        {
            "nombre": "Papas Fritas Medianas",
            "descripcion": "Papas fritas crujientes con sal y especias",
            "precio": 650.00,
            "imagen_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400",
            "stock": 100,
            "activo": True,
            "categoria_nombre": "Acompañamientos",
            "ingrediente_nombres": ["Papa", "Sal", "Aceite"],
        },
        {
            "nombre": "Aros de Cebolla",
            "descripcion": "Aros de cebolla rebozados y fritos",
            "precio": 750.00,
            "imagen_url": "https://images.unsplash.com/photo-1639024471283-03518883512d?w=400",
            "stock": 40,
            "activo": True,
            "categoria_nombre": "Acompañamientos",
            "ingrediente_nombres": ["Cebolla", "Harina", "Huevos", "Aceite"],
        },
        {
            "nombre": "Coca-Cola 500ml",
            "descripcion": "Bebida gaseosa cola",
            "precio": 450.00,
            "imagen_url": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400",
            "stock": 200,
            "activo": True,
            "categoria_nombre": "Bebidas",
            "ingrediente_nombres": ["Agua", "Azúcar", "Carbonato"],
        },
        {
            "nombre": "Sprite 500ml",
            "descripcion": "Bebida gaseosa lima-limón",
            "precio": 450.00,
            "imagen_url": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400",
            "stock": 150,
            "activo": True,
            "categoria_nombre": "Bebidas",
            "ingrediente_nombres": ["Agua", "Azúcar", "Carbonato"],
        },
        {
            "nombre": "Agua Mineral 500ml",
            "descripcion": "Agua mineral sin gas",
            "precio": 300.00,
            "imagen_url": "https://images.unsplash.com/photo-1559839914-17aae19cec71?w=400",
            "stock": 100,
            "activo": True,
            "categoria_nombre": "Bebidas",
            "ingrediente_nombres": ["Agua"],
        },
        {
            "nombre": "Flan con Caramelo",
            "descripcion": "Postre flan de vainilla con salsa de caramelo",
            "precio": 550.00,
            "imagen_url": "https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?w=400",
            "stock": 20,
            "activo": True,
            "categoria_nombre": "Postres",
            "ingrediente_nombres": ["Leche", "Huevos", "Azúcar", "Esencia de vainilla"],
        },
        {
            "nombre": "Brownie de Chocolate",
            "descripcion": "Brownie caliente con nueces y helado de vainilla",
            "precio": 650.00,
            "imagen_url": "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=400",
            "stock": 15,
            "activo": True,
            "categoria_nombre": "Postres",
            "ingrediente_nombres": ["Chocolate", "Harina", "Huevos", "Nueces", "Mantequilla"],
        },
    ]

    # Obtener categorías e ingredientes existentes
    from app.modules.categorias.model import Categoria
    from app.modules.ingredientes.model import Ingrediente

    # Obtener categorías por nombre
    statement = select(Categoria).where(Categoria.activa == True)
    categorias_existentes = {cat.nombre: cat.id for cat in session.exec(statement).all()}

    # Obtener ingredientes por nombre
    statement = select(Ingrediente).where(Ingrediente.eliminado_en == None)
    ingredientes_existentes = {ing.nombre: ing.id for ing in session.exec(statement).all()}

    # Crear productos
    for prod_data in productos_data:
        categoria_nombre = prod_data.pop("categoria_nombre")
        ingrediente_nombres = prod_data.pop("ingrediente_nombres")

        # Buscar o crear categoría
        categoria_id = categorias_existentes.get(categoria_nombre)
        if categoria_id is None:
            # Crear categoría si no existe
            from app.modules.categorias.model import Categoria
            import re
            slug = re.sub(r'[^a-z0-9]', '-', categoria_nombre.lower()).strip('-')
            nueva_cat = Categoria(
                nombre=categoria_nombre,
                slug=slug,
                activa=True,
            )
            session.add(nueva_cat)
            session.flush()
            categoria_id = nueva_cat.id
            categorias_existentes[categoria_nombre] = categoria_id

        # Crear producto
        producto = Producto(**prod_data)
        session.add(producto)
        session.flush()

        # Asociar categoría
        rel_cat = ProductoCategoria(producto_id=producto.id, categoria_id=categoria_id)
        session.add(rel_cat)

        # Buscar o crear ingredientes y asociarlos
        for ing_nombre in ingrediente_nombres:
            ingrediente_id = ingredientes_existentes.get(ing_nombre)
            if ingrediente_id is None:
                # Crear ingrediente si no existe (parasimplificar)
                from app.modules.ingredientes.model import Ingrediente
                nuevo_ing = Ingrediente(
                    nombre=ing_nombre,
                    descripcion=f"Ingrediente: {ing_nombre}",
                    eliminado_en=None,
                )
                session.add(nuevo_ing)
                session.flush()
                ingrediente_id = nuevo_ing.id
                ingredientes_existentes[ing_nombre] = ingrediente_id

            # Asociar ingrediente
            rel_ing = ProductoIngrediente(
                producto_id=producto.id,
                ingrediente_id=ingrediente_id,
            )
            session.add(rel_ing)

        print(f"  ✓ Producto creado: {producto.nombre}")

    print(f"  ✓ Seed de productos completado: {len(productos_data)} productos")


if __name__ == "__main__":
    print("Iniciando seed de datos...")
    run_seed()
