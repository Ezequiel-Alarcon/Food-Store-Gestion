"""merge_008_and_apellido

Revision ID: 7cc416400224
Revises: 008, 40a50a4d0f4c
Create Date: 2026-05-16 22:32:10.367030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cc416400224'
down_revision: Union[str, None] = ('008', '40a50a4d0f4c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass