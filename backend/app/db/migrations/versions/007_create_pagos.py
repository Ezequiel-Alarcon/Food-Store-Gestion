"""create_pagos_table

Revision ID: 007
Revises: 006
Create Date: 2026-05-12

Crea tabla: pagos.
Relacion 1:N Pedido->Pago (multiples intentos de pago permitidos).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear tabla pagos."""
    op.create_table(
        'pagos',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('mp_payment_id', sa.BigInteger(), nullable=True),
        sa.Column('idempotency_key', sa.String(length=64), nullable=False),
        sa.Column('external_reference', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='pending'),
        sa.Column('status_detail', sa.String(length=100), nullable=True),
        sa.Column('payment_method_id', sa.String(length=30), nullable=True),
        sa.Column('transaction_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), nullable=False),

        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mp_payment_id'),
        sa.UniqueConstraint('idempotency_key'),
        sa.UniqueConstraint('external_reference'),
    )
    op.create_index('ix_pagos_pedido_id', 'pagos', ['pedido_id'])


def downgrade() -> None:
    """Eliminar tabla pagos."""
    op.drop_index('ix_pagos_pedido_id', table_name='pagos')
    op.drop_table('pagos')
