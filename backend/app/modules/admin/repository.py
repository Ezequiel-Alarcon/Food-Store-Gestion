"""app.modules.admin.repository

Repositorio para métricas agregadas del dashboard admin.
Usa BaseRepository como patrón base, pero las queries son aggregates
que no encajan en el CRUD genérico — se implementan directamente.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
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
        # dialect puede ser string ('sqlite') o un Dialect Object con .name
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

    def get_general_metrics(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> dict[str, Any]:
        """Retorna métricas generales: total_pedidos, total_revenue, ticket_promedio, total_clientes.

        Solo cuenta pedidos en estados TERMINALES: ENTREGADO y CONFIRMADO.
        """
        completed_states = ("ENTREGADO", "CONFIRMADO")

        query = (
            select(
                func.count(Pedido.id),
                func.coalesce(func.sum(Pedido.total), 0.0),
            )
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
        )

        if desde:
            query = query.where(Pedido.creado_en >= desde)
        if hasta:
            query = query.where(Pedido.creado_en <= hasta)

        pedido_stats = self.session.exec(query).one()

        total_pedidos = int(pedido_stats[0] or 0)
        total_revenue = float(pedido_stats[1] or 0.0)
        ticket_promedio = round(total_revenue / total_pedidos, 2) if total_pedidos > 0 else 0.0

        # Unique clients
        clientes_query = (
            select(func.count(func.distinct(Pedido.cliente_id)))
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
        )
        if desde:
            clientes_query = clientes_query.where(Pedido.creado_en >= desde)
        if hasta:
            clientes_query = clientes_query.where(Pedido.creado_en <= hasta)

        total_clientes = self.session.exec(clientes_query).one()[0] or 0

        return {
            "total_pedidos": total_pedidos,
            "total_revenue": round(total_revenue, 2),
            "ticket_promedio": ticket_promedio,
            "total_clientes": int(total_clientes),
        }

    def get_sales_chart(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna revenue y count diario del rango especificado.

        Si no se pasan desde/hasta, usa default últimos 30 días.
        Solo incluye pedidos en estados TERMINALES: ENTREGADO y CONFIRMADO.
        """
        completed_states = ("ENTREGADO", "CONFIRMADO")

        if desde is None:
            desde = datetime.now(timezone.utc) - timedelta(days=30)

        day_col = _date_trunc_day(self.session, Pedido.creado_en)

        query = (
            select(
                day_col.label("fecha"),
                func.count(Pedido.id).label("total_pedidos"),
                func.coalesce(func.sum(Pedido.total), 0.0).label("revenue"),
            )
            .select_from(Pedido)
            .where(Pedido.estado_codigo.in_(completed_states))
            .where(Pedido.creado_en >= desde)
            .group_by(day_col)
            .order_by(day_col.asc())
        )

        if hasta:
            query = query.where(Pedido.creado_en <= hasta)

        rows = self.session.exec(query).all()

        return [
            {
                "fecha": row.fecha,
                "total_pedidos": int(row.total_pedidos or 0),
                "revenue": round(float(row.revenue or 0.0), 2),
            }
            for row in rows
        ]

    def get_top_products(
        self,
        limit: int = 10,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna los productos más vendidos (por cantidad total).

        JOIN detalle_pedido + producto + pedido para filtro temporal.
        Solo cuenta productos activos.
        """
        base_query = (
            select(
                DetallePedido.producto_id,
                Producto.nombre,
                func.sum(DetallePedido.cantidad).label("cantidad_vendida"),
            )
            .join(Producto, Producto.id == DetallePedido.producto_id)
            .join(Pedido, Pedido.id == DetallePedido.pedido_id)
            .where(Producto.activo == True)  # noqa: E712
        )

        if desde:
            base_query = base_query.where(Pedido.creado_en >= desde)
        if hasta:
            base_query = base_query.where(Pedido.creado_en <= hasta)

        query = (
            base_query
            .group_by(DetallePedido.producto_id, Producto.nombre)
            .order_by(func.sum(DetallePedido.cantidad).desc())
            .limit(limit)
        )

        rows = self.session.exec(query).all()

        return [
            {
                "producto_id": int(row.producto_id),
                "nombre": row.nombre,
                "cantidad_vendida": int(row.cantidad_vendida or 0),
            }
            for row in rows
        ]

    def get_orders_by_status(
        self,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna conteo de pedidos agrupados por estado_codigo."""
        query = (
            select(
                Pedido.estado_codigo,
                func.count(Pedido.id).label("cantidad"),
            )
            .select_from(Pedido)
            .group_by(Pedido.estado_codigo)
            .order_by(Pedido.estado_codigo.asc())
        )

        if desde:
            query = query.where(Pedido.creado_en >= desde)
        if hasta:
            query = query.where(Pedido.creado_en <= hasta)

        rows = self.session.exec(query).all()

        return [
            {
                "estado_codigo": row.estado_codigo,
                "cantidad": int(row.cantidad or 0),
            }
            for row in rows
        ]

    def get_total_usuarios_registrados(self) -> int:
        """Retorna el conteo total de usuarios registrados."""
        from app.modules.auth.model import Usuario

        result = self.session.exec(select(func.count(Usuario.id))).one()
        return int(result[0] or 0)
