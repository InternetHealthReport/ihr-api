import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.database import Base
import importlib.util
import pathlib

# Get Alembic config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Automatically discover and import models
models_path = pathlib.Path(__file__).parent.parent / "models"
sys.path.append(str(models_path.parent))  # Ensure parent directory is in path

for file in models_path.glob("*.py"):
    if file.name != "__init__.py":
        module_name = f"models.{file.stem}"
        importlib.import_module(module_name)

# Set target metadata to Base
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    # Prevent dropping tables and indexes
    if reflected and compare_to is None:
        if type_ in ("table", "index"):
            return False  # Don't drop it
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,  # detect type changes (e.g. from Int to BigInt)
        # detect default value changes of a column(will apply to newly inserted records)
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata,
                          include_object=include_object,
                          compare_type=True,
                          compare_server_default=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
