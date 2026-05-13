"""app.modules.admin.repository

Repositorio para métricas agregadas del dashboard admin.
Usa BaseRepository como patrón base, pero las queries son aggregates
que no encajan en el CRUD genérico — se implementan directamente.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from app.core.repository import BaseRepository
from app.modules.pedidos.model import DetallePedido, Pedido
from app.modules.productos.model import Producto


def _is_sqlite(session: Session) -> bool:
    """Detecta si la sesión usa SQLite (para tests)."""
    try:
        dialect = session.bind.dialect
        # dialect puede ser string ('sqlite') o un Dialect object con .name
        if isinstance(dialect, str):
            return dialect in ("sqlite", "aiosqlite")
        # Para Dialect objects (SQLAlchemy 2.x)
        dialect_name = getattr(dialect, "name", None)
        if dialect_name:
            return dialect_name in ("sqlite", "aiosqlite")
        return False
    except Exception:
        return False


def _date_trunc_day(session: Session, column) -> Any:
    """Retorna la expresión correcta para truncar a día según el dialecto."""
    if _is_sqlite(session):
        # SQLite: date() trunca a YYYY-MM-DD
        return func.date(column)
    # PostgreSQL
    return func.date_trunc("day", column)


class AdminRepository:
    """Repositorio para métricas agregadas del dashboard."""

    def __init__(self, session: Session):
        self.session = session

    def get_general_metrics(self) -> dict[str, Any]:
        """Retorna métricas generales: total_pedidos, total_revenue, ticket_promedio, total_clientes.

        Solo cuenta pedidos en estados TERMINALES: ENTREGADO y CONFIRMADO.
        """
        completed_states = ("ENTREGADO", "CONFIRMADO")

        # Count and sum
        pedido_stats = self.session.exec(
            select(
                func.count(Pedido.id),
                func.coalesce(func.sum(Pedido.total), 0.0),
            )
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
        ).one()

        total_pedidos = int(pedido_stats[0] or 0)
        total_revenue = float(pedido_stats[1] or 0.0)
        ticket_promedio = round(total_revenue / total_pedidos, 2) if total_pedidos > 0 else 0.0

        # Unique clients
        total_clientes = self.session.exec(
            select(func.count(func.distinct(Pedido.cliente_id)))
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
        ).one()[0] or 0

        return {
            "total_pedidos": total_pedidos,
            "total_revenue": round(total_revenue, 2),
            "ticket_promedio": ticket_promedio,
            "total_clientes": int(total_clientes),
        }

    def get_sales_chart(self, days: int = 30) -> list[dict[str, Any]]:
        """Retorna revenue y count diario de los últimos `days` días.

        Solo incluye pedidos en estados TERMINALES: ENTREGADO y CONFIRMADO.
        """
        completed_states = ("ENTREGADO", "CONFIRMADO")
        since = datetime.utcnow() - timedelta(days=days)

        day_col = _date_trunc_day(self.session, Pedido.creado_en)

        rows = self.session.exec(
            select(
                day_col.label("fecha"),
                func.count(Pedido.id).label("total_pedidos"),
                func.coalesce(func.sum(Pedido.total), 0.0).label("revenue"),
            )
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
            .where(Pedido.creado_en >= since)
            .group_by(day_col)
            .order_by(day_col.asc())
        ).all()

        return [
            {
                "fecha": row.fecha,
                "total_pedidos": int(row.total_pedidos or 0),
                "revenue": round(float(row.revenue or 0.0), 2),
            }
            for row in rows
        ]

    def get_top_products(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retorna los productos más vendidos (por cantidad total).

        JOIN detalle_pedido + producto, sin filtro temporal.
        Solo cuenta productos activos.
        """
        rows = self.session.exec(
            select(
                DetallePedido.producto_id,
                Producto.nombre,
                func.sum(DetallePedido.cantidad).label("cantidad_vendida"),
            )
            .join(Producto, Producto.id == DetallePedido.producto_id)
            .where(Producto.activo == True)  # noqa: E712
            .group_by(DetallePedido.producto_id, Producto.nombre)
            .order_by(func.sum(DetallePedido.cantidad).desc())
            .limit(limit)
        ).all()

        return [
            {
                "producto_id": int(row.producto_id),
                "nombre": row.nombre,
                "cantidad_vendida": int(row.cantidad_vendida or 0),
            }
            for row in rows
        ]

    def get_orders_by_status(self) -> list[dict[str, Any]]:
        """Retorna conteo de pedidos agrupados por estado_codigo."""
        rows = self.session.exec(
            select(
                Pedido.estado_codigo,
                func.count(Pedido.id).label("cantidad"),
            )
            .select_from(Pedido)
            .group_by(Pedido.estado_codigo)
            .order_by(Pedido.estado_codigo.asc())
        ).all()

        return [
            {
                "estado_codigo": row.estado_codigo,
                "cantidad": int(row.cantidad or 0),
            }
            for row in rows
        ]