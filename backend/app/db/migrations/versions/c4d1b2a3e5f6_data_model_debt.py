"""data-model-debt: es_principal, es_removible, eliminado_en, unique nombre

Revision ID: c4d1b2a3e5f6
Revises: 40a50a4d0f4c
Create Date: 2026-05-18
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c4d1b2a3e5f6'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. ProductoCategoria: agregar es_principal
    op.add_column(
        'producto_categorias',
        sa.Column('es_principal', sa.Boolean(), nullable=False, server_default=sa.text('false'))
    )

    # 2. ProductoIngrediente: agregar es_removible
    op.add_column(
        'producto_ingredientes',
        sa.Column('es_removible', sa.Boolean(), nullable=False, server_default=sa.text('false'))
    )

    # 3. Categoria: activa → eliminado_en
    op.add_column(
        'categorias',
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True)
    )
    # Migrar datos: categorías con activa=false → eliminado_en=now()
    op.execute(
        "UPDATE categorias SET eliminado_en = NOW() WHERE activa = false"
    )
    # Dropear columna vieja
    op.drop_column('categorias', 'activa')

    # 4. Ingrediente: unique index parcial en nombre
    op.create_index(
        'ix_ingredientes_nombre_active',
        'ingredientes',
        ['nombre'],
        unique=True,
        postgresql_where=sa.text('eliminado_en IS NULL')
    )


def downgrade() -> None:
    # 4. Revertir unique index
    op.drop_index('ix_ingredientes_nombre_active', table_name='ingredientes')

    # 3. Revertir categoria: eliminado_en → activa
    op.add_column(
        'categorias',
        sa.Column('activa', sa.Boolean(), nullable=False, server_default=sa.text('true'))
    )
    op.execute(
        "UPDATE categorias SET activa = (eliminado_en IS NULL)"
    )
    op.drop_column('categorias', 'eliminado_en')

    # 2. Revertir es_removible
    op.drop_column('producto_ingredientes', 'es_removible')

    # 1. Revertir es_principal
    op.drop_column('producto_categorias', 'es_principal')
