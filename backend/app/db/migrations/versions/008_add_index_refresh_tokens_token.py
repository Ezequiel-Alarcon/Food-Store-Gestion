"""add_index_refresh_tokens_token

Revision ID: 008
Revises: 007
Create Date: 2026-05-15

Agrega índice en la columna token de la tabla refresh_tokens
para optimizar búsquedas por token.
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Agregar índice en refresh_tokens.token."""
    op.create_index('ix_refresh_tokens_token', 'refresh_tokens', ['token'])


def downgrade() -> None:
    """Eliminar índice en refresh_tokens.token."""
    op.drop_index('ix_refresh_tokens_token', table_name='refresh_tokens')
