"""add_apellido_and_timestamptz

Revision ID: 40a50a4d0f4c
Revises: 007
Create Date: 2026-05-13 13:49:35.427066

Agrega columna apellido a usuarios y convierte datetime a TIMESTAMPTZ.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a50a4d0f4c'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar columna apellido a usuarios
    op.add_column(
        'usuarios',
        sa.Column('apellido', sa.String(), nullable=False, server_default='')
    )

    # Convertir datetime columns a TIMESTAMPTZ en usuarios
    op.alter_column(
        'usuarios', 'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        'usuarios', 'updated_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="updated_at AT TIME ZONE 'UTC'"
    )

    # Convertir datetime columns a TIMESTAMPTZ en refresh_tokens
    op.alter_column(
        'refresh_tokens', 'expires_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="expires_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        'refresh_tokens', 'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )


def downgrade() -> None:
    # Revertir TIMESTAMPTZ → DateTime en refresh_tokens
    op.alter_column(
        'refresh_tokens', 'created_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )
    op.alter_column(
        'refresh_tokens', 'expires_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )

    # Revertir TIMESTAMPTZ → DateTime en usuarios
    op.alter_column(
        'usuarios', 'updated_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )
    op.alter_column(
        'usuarios', 'created_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )

    # Eliminar columna apellido
    op.drop_column('usuarios', 'apellido')