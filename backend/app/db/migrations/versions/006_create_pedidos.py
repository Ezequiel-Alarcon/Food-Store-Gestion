"""create_pedidos_module

Revision ID: 006
Revises: 005
Create Date: 2026-05-12

Crea tablas: estados_pedido, pedidos, detalle_pedido, historial_estado_pedido.
Los estados se seedean en app/db/seed.py (no en esta migración).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear tablas del módulo de pedidos."""

    # ── Tabla de lookup: estados_pedido ──────────────────────────────
    op.create_table(
        'estados_pedido',
        sa.Column('codigo', sa.String(length=30), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.String(length=500), nullable=True),
        sa.Column('orden', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('es_terminal', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('codigo'),
    )

    # ── Tabla principal: pedidos ─────────────────────────────────────
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('estado_codigo', sa.String(length=30), nullable=False, server_default='PENDIENTE'),

        # Snapshot dirección
        sa.Column('direccion_calle', sa.String(length=120), nullable=False),
        sa.Column('direccion_numero', sa.String(length=30), nullable=False),
        sa.Column('direccion_piso_depto', sa.String(length=60), nullable=True),
        sa.Column('direccion_ciudad', sa.String(length=120), nullable=False),
        sa.Column('direccion_provincia', sa.String(length=120), nullable=False),
        sa.Column('direccion_codigo_postal', sa.String(length=20), nullable=True),
        sa.Column('direccion_pais', sa.String(length=120), nullable=False, server_default='Argentina'),
        sa.Column('direccion_referencias', sa.String(length=500), nullable=True),

        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('costo_envio', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), nullable=False),

        sa.ForeignKeyConstraint(['cliente_id'], ['usuarios.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['estado_codigo'], ['estados_pedido.codigo'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_pedidos_cliente_id', 'pedidos', ['cliente_id'])
    op.create_index('ix_pedidos_estado_codigo', 'pedidos', ['estado_codigo'])

    # ── Tabla: detalle_pedido ────────────────────────────────────────
    op.create_table(
        'detalle_pedido',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('precio_unitario', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('exclusiones', postgresql.ARRAY(sa.Integer()), nullable=False, server_default='{}'),

        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_detalle_pedido_pedido_id', 'detalle_pedido', ['pedido_id'])

    # ── Tabla: historial_estado_pedido (append-only) ─────────────────
    op.create_table(
        'historial_estado_pedido',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('estado_anterior_codigo', sa.String(length=30), nullable=True),
        sa.Column('estado_nuevo_codigo', sa.String(length=30), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=True),
        sa.Column('actor_tipo', sa.String(length=20), nullable=False, server_default='USUARIO'),
        sa.Column('motivo', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=False),

        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['estado_anterior_codigo'], ['estados_pedido.codigo'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['estado_nuevo_codigo'], ['estados_pedido.codigo'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['actor_id'], ['usuarios.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_historial_estado_pedido_pedido_id', 'historial_estado_pedido', ['pedido_id'])


def downgrade() -> None:
    """Eliminar tablas del módulo de pedidos (orden inverso)."""
    op.drop_index('ix_historial_estado_pedido_pedido_id', table_name='historial_estado_pedido')
    op.drop_table('historial_estado_pedido')

    op.drop_index('ix_detalle_pedido_pedido_id', table_name='detalle_pedido')
    op.drop_table('detalle_pedido')

    op.drop_index('ix_pedidos_estado_codigo', table_name='pedidos')
    op.drop_index('ix_pedidos_cliente_id', table_name='pedidos')
    op.drop_table('pedidos')

    op.drop_table('estados_pedido')
