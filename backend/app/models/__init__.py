"""
Models package - re-exporta todos los modelos SQLModel de los módulos.
Los modelos se van populando a medida que se implementan los módulos.
"""
# Importar modelos de cada módulo cuando estén implementados
# El orden importa por dependencias (ForeignKey)

# Dominio 1: Identidad y Acceso
try:
    from app.modules.auth.model import Usuario, Rol, UsuarioRol
except ImportError:
    pass

try:
    from app.modules.refreshtokens.model import RefreshToken
except ImportError:
    pass

try:
    from app.modules.direcciones.model import DireccionEntrega
except ImportError:
    pass

# Dominio 2: Catálogo de Productos
try:
    from app.modules.categorias.model import Categoria
except ImportError:
    pass

try:
    from app.modules.ingredientes.model import Ingrediente, ProductoIngrediente
except ImportError:
    pass

try:
    from app.modules.productos.model import Producto, ProductoCategoria
except ImportError:
    pass

# Dominio 3: Ventas, Pagos y Trazabilidad
try:
    from app.modules.pagos.model import FormaPago, Pago
except ImportError:
    pass

try:
    from app.modules.pedidos.model import EstadoPedido, Pedido, DetallePedido, HistorialEstadoPedido
except ImportError:
    pass


__all__ = [
    # Dominio 1
    "Usuario",
    "Rol",
    "UsuarioRol",
    "RefreshToken",
    "DireccionEntrega",
    # Dominio 2
    "Categoria",
    "Ingrediente",
    "ProductoIngrediente",
    "Producto",
    "ProductoCategoria",
    # Dominio 3
    "FormaPago",
    "Pago",
    "EstadoPedido",
    "Pedido",
    "DetallePedido",
    "HistorialEstadoPedido",
]