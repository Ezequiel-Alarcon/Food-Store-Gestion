"""
Alembic environment configuration.
Importa todos los modelos para que Alembic pueda detectarlos.
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import get_settings
from app.core.database import SQLModel

# Importar todos los modelos para que Alembic los detecte
# Los imports se van agregando a medida que se implementan los módulos
from app.modules.auth.model import Usuario  # noqa: F401
from app.modules.refreshtokens.model import RefreshToken  # noqa: F401

# Modelos pendientes — se activan cuando se implementen:
# from app.modules.direcciones.model import DireccionEntrega  # noqa: F401
# from app.modules.categorias.model import Categoria  # noqa: F401
# from app.modules.productos.model import Producto, ProductoCategoria  # noqa: F401
# from app.modules.ingredientes.model import Ingrediente, ProductoIngrediente  # noqa: F401
from app.modules.pedidos.model import Pedido, DetallePedido, HistorialEstadoPedido, EstadoPedido  # noqa: F401
# from app.modules.pagos.model import Pago, FormaPago  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configurar URL de base de datos desde settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()