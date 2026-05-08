"""create sucursales, user_addresses, branch_addresses

Revision ID: 004
Revises: 003
Create Date: 2026-05-08

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sucursales
    op.create_table(
        "sucursales",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sucursales_nombre", "sucursales", ["nombre"])
    op.create_index("ix_sucursales_activa", "sucursales", ["activa"])

    # user_addresses
    op.create_table(
        "user_addresses",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("etiqueta", sa.String(length=60), nullable=True),
        sa.Column("calle", sa.String(length=120), nullable=False),
        sa.Column("numero", sa.String(length=30), nullable=False),
        sa.Column("piso_depto", sa.String(length=60), nullable=True),
        sa.Column("ciudad", sa.String(length=120), nullable=False),
        sa.Column("provincia", sa.String(length=120), nullable=False),
        sa.Column("codigo_postal", sa.String(length=20), nullable=True),
        sa.Column("pais", sa.String(length=120), nullable=False),
        sa.Column("referencias", sa.String(length=500), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["usuarios.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_user_addresses_user_id", "user_addresses", ["user_id"])
    op.create_index("ix_user_addresses_activa", "user_addresses", ["activa"])

    # default address: 1 por usuario (solo activa)
    op.execute(
        """
        CREATE UNIQUE INDEX uix_user_addresses_default_activa
        ON user_addresses (user_id)
        WHERE is_default = true AND activa = true
        """
    )

    # branch_addresses
    op.create_table(
        "branch_addresses",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("branch_id", sa.Integer(), nullable=False),
        sa.Column("calle", sa.String(length=120), nullable=False),
        sa.Column("numero", sa.String(length=30), nullable=False),
        sa.Column("piso_depto", sa.String(length=60), nullable=True),
        sa.Column("ciudad", sa.String(length=120), nullable=False),
        sa.Column("provincia", sa.String(length=120), nullable=False),
        sa.Column("codigo_postal", sa.String(length=20), nullable=True),
        sa.Column("pais", sa.String(length=120), nullable=False),
        sa.Column("referencias", sa.String(length=500), nullable=True),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["branch_id"], ["sucursales.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_branch_addresses_branch_id", "branch_addresses", ["branch_id"])
    op.create_index("ix_branch_addresses_activa", "branch_addresses", ["activa"])

    # 1 address activa por sucursal (permite historico por soft-delete)
    op.execute(
        """
        CREATE UNIQUE INDEX uix_branch_addresses_branch_activa
        ON branch_addresses (branch_id)
        WHERE activa = true
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uix_branch_addresses_branch_activa")
    op.drop_index("ix_branch_addresses_activa", table_name="branch_addresses")
    op.drop_index("ix_branch_addresses_branch_id", table_name="branch_addresses")
    op.drop_table("branch_addresses")

    op.execute("DROP INDEX IF EXISTS uix_user_addresses_default_activa")
    op.drop_index("ix_user_addresses_activa", table_name="user_addresses")
    op.drop_index("ix_user_addresses_user_id", table_name="user_addresses")
    op.drop_table("user_addresses")

    op.drop_index("ix_sucursales_activa", table_name="sucursales")
    op.drop_index("ix_sucursales_nombre", table_name="sucursales")
    op.drop_table("sucursales")
