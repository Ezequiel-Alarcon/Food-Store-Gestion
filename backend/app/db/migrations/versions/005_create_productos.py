"""create_productos_table

Revision ID: 005
Revises: 004
Create Date: 2026-05-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear tabla productos y tablas de relación."""
    # Tabla productos
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('descripcion', sa.String(length=2000), nullable=True),
        sa.Column('precio', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('imagen_url', sa.String(length=500), nullable=True),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('eliminado_en', sa.DateTime(), nullable=True),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    # Índice en nombre para búsquedas
    op.create_index('ix_productos_nombre', 'productos', ['nombre'])

    # Índice en activo para filtros
    op.create_index('ix_productos_activo', 'productos', ['activo'])

    # Índice en eliminado_en para soft-delete
    op.create_index('ix_productos_eliminado_en', 'productos', ['eliminado_en'])

    # Tabla de relación producto-categoría (muchos a muchos)
    op.create_table(
        'producto_categorias',
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('categoria_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('producto_id', 'categoria_id'),
    )

    # Índice en categoria_id
    op.create_index('ix_producto_categorias_categoria_id', 'producto_categorias', ['categoria_id'])

    # Tabla de relación producto-ingrediente (muchos a muchos)
    op.create_table(
        'producto_ingredientes',
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('ingrediente_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingrediente_id'], ['ingredientes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('producto_id', 'ingrediente_id'),
    )

    # Índice en ingrediente_id
    op.create_index('ix_producto_ingredientes_ingrediente_id', 'producto_ingredientes', ['ingrediente_id'])


def downgrade() -> None:
    """Eliminar tablas de productos."""
    op.drop_index('ix_producto_ingredientes_ingrediente_id', table_name='producto_ingredientes')
    op.drop_table('producto_ingredientes')
    op.drop_index('ix_producto_categorias_categoria_id', table_name='producto_categorias')
    op.drop_table('producto_categorias')
    op.drop_index('ix_productos_eliminado_en', table_name='productos')
    op.drop_index('ix_productos_activo', table_name='productos')
    op.drop_index('ix_productos_nombre', table_name='productos')
    op.drop_table('productos')