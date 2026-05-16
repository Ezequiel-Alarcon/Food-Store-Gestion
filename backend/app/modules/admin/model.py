"""app.modules.admin.model

Modelos re-exportados que el módulo admin consulta.
Admin es un módulo transversal — no tiene tablas propias.
"""
from app.modules.auth.model import Usuario
from app.modules.pedidos.model import DetallePedido, HistorialEstadoPedido, Pedido
from app.modules.productos.model import Producto

__all__ = ["Pedido", "DetallePedido", "HistorialEstadoPedido", "Producto", "Usuario"]
