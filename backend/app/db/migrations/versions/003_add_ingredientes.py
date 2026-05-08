"""add_ingredientes_table

Revision ID: 003
Revises: 002
Create Date: 2026-05-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear tabla ingredientes con constraints."""
    op.create_table(
        'ingredientes',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.String(length=500), nullable=True),
        sa.Column('es_alergeno', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), nullable=True),
        sa.Column('eliminado_en', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Índice en nombre para búsquedas
    op.create_index('ix_ingredientes_nombre', 'ingredientes', ['nombre'])

    # Índice en es_alergeno para filtros
    op.create_index('ix_ingredientes_es_alergeno', 'ingredientes', ['es_alergeno'])

    # Índice en eliminado_en para soft-delete
    op.create_index('ix_ingredientes_eliminado_en', 'ingredientes', ['eliminado_en'])

    # Índice único en nombre (solo para no eliminados)
    op.execute("""
        CREATE UNIQUE INDEX uix_ingredientes_nombre_no_eliminado
        ON ingredientes (nombre)
        WHERE eliminado_en IS NULL
    """)


def downgrade() -> None:
    """Eliminar tabla ingredientes."""
    op.execute("DROP INDEX IF EXISTS uix_ingredientes_nombre_no_eliminado")
    op.drop_index('ix_ingredientes_eliminado_en', table_name='ingredientes')
    op.drop_index('ix_ingredientes_es_alergeno', table_name='ingredientes')
    op.drop_index('ix_ingredientes_nombre', table_name='ingredientes')
    op.drop_table('ingredientes')