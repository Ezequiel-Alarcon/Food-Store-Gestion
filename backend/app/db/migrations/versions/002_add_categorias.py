"""add_categorias_table

Revision ID: 002
Revises: 001
Create Date: 2026-05-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear tabla categorias con constraints."""
    # Tabla categorias
    op.create_table(
        'categorias',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('descripcion', sa.String(length=500), nullable=True),
        sa.Column('padre_id', sa.Integer(), nullable=True),
        sa.Column('orden', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('activa', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    # Índice único en slug
    op.create_index('ix_categorias_slug', 'categorias', ['slug'], unique=True)

    # Índice en padre_id
    op.create_index('ix_categorias_padre_id', 'categorias', ['padre_id'])

    # Índice en activa
    op.create_index('ix_categorias_activa', 'categorias', ['activa'])

    # Foreign key auto-referencial
    op.create_foreign_key(
        'fk_categorias_padre_id',
        'categorias', 'categorias',
        ['padre_id'], ['id'],
        ondelete='SET NULL',
    )

    # Constraint único: nombre + padre_id cuando activa = true
    # Esto requiere un índice único parcial
    op.execute("""
        CREATE UNIQUE INDEX uix_categorias_nombre_padre_activa
        ON categorias (nombre, padre_id)
        WHERE activa = true
    """)


def downgrade() -> None:
    """Eliminar tabla categorias."""
    op.execute("DROP INDEX IF EXISTS uix_categorias_nombre_padre_activa")
    op.drop_constraint('fk_categorias_padre_id', 'categorias', type_='foreignkey')
    op.drop_index('ix_categorias_activa', table_name='categorias')
    op.drop_index('ix_categorias_padre_id', table_name='categorias')
    op.drop_index('ix_categorias_slug', table_name='categorias')
    op.drop_table('categorias')