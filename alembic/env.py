import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.database import Base
import importlib.util
import pathlib
from alembic.operations import ops

# Get Alembic config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modify the model discovery section
models_path = pathlib.Path(__file__).parent.parent / "models"
sys.path.append(str(models_path.parent))

model_classes = []

# First pass: Load all models
for file in models_path.glob("*.py"):
    if file.name != "__init__.py":
        module_name = f"models.{file.stem}"
        module = importlib.import_module(module_name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Base) and attr != Base:
                model_classes.append(attr)

# Set target metadata
target_metadata = Base.metadata

# Second pass: Associate metadata (hypertable and indexes) with table objects
for model in model_classes:
    table = target_metadata.tables.get(model.__tablename__)
    if table is not None:
        # Associate hypertable metadata
        if hasattr(model, '__hypertable__'):
            setattr(table, '__hypertable__', model.__hypertable__)

        # Associate indexes metadata
        if hasattr(model, '__indexes__'):
            setattr(table, '__indexes__', model.__indexes__)


def include_object(object, name, type_, reflected, compare_to):
    # Prevent dropping tables and indexes
    if reflected and compare_to is None:
        if type_ in ("table", "index"):
            return False  # Don't drop it
    return True


def process_revision_directives(context, revision, directives):
    """Called during 'alembic revision --autogenerate'"""
    if directives[0].upgrade_ops is not None:
        # Process create table operations and inject hypertable commands
        process_ops(
            context,  directives[0].upgrade_ops, directives[0].downgrade_ops)


def create_hypertable_ops(table_name, hypertable_meta, is_existing=False):
    """Generate hypertable creation operations."""
    upgrade_ops = []
    downgrade_ops = []

    time_col = hypertable_meta['time_column']
    chunk_interval = hypertable_meta.get('chunk_time_interval', '1 day')

    # Create hypertable with migrate_data for existing tables
    hypertable_sql = (
        f"SELECT create_hypertable('{table_name}', by_range('{time_col}', INTERVAL '{chunk_interval}'));"
    )

    upgrade_ops.append(ops.ExecuteSQLOp(hypertable_sql))

    # Handle compression
    if hypertable_meta.get('compress', False):
        segment_by = hypertable_meta.get('compress_segmentby', '')
        order_by = hypertable_meta.get('compress_orderby', time_col)
        compress_sql = (
            f"ALTER TABLE {table_name} SET ("
            f"timescaledb.compress, "
            f"timescaledb.compress_segmentby = '{segment_by}', "
            f"timescaledb.compress_orderby = '{order_by}'"
            f");"
        )
        upgrade_ops.append(ops.ExecuteSQLOp(compress_sql))
        downgrade_ops.append(
            ops.ExecuteSQLOp(
                f"ALTER TABLE {table_name} SET (timescaledb.compress = false);"
            )
        )

    # Handle compression policy
    if hypertable_meta.get('compress_policy', False):
        compress_after = hypertable_meta.get('compress_after', '7 days')
        policy_sql = (
            f"SELECT add_compression_policy('{table_name}', "
            f"INTERVAL '{compress_after}');"
        )
        upgrade_ops.append(ops.ExecuteSQLOp(policy_sql))
        downgrade_ops.append(
            ops.ExecuteSQLOp(
                f"SELECT remove_compression_policy('{table_name}', if_exists => TRUE);"
            )
        )

    return upgrade_ops, downgrade_ops


def create_index_ops(table_name, indexes_meta):
    """Generate index creation operations."""
    upgrade_ops = []
    downgrade_ops = []

    for idx in indexes_meta:
        col_list = ', '.join(idx['columns'])
        create_index_sql = f"CREATE INDEX IF NOT EXISTS {idx['name']} ON {table_name} ({col_list});"
        upgrade_ops.append(ops.ExecuteSQLOp(create_index_sql))

        drop_index_sql = f"DROP INDEX IF EXISTS {idx['name']};"
        downgrade_ops.append(ops.ExecuteSQLOp(drop_index_sql))

    return upgrade_ops, downgrade_ops


def process_ops(context, upgrade_ops, downgrade_ops):
    """Process upgrade and downgrade operations."""
    final_upgrade_ops = []
    final_downgrade_ops = []

    # First pass: Handle table creations and their features
    for op_ in upgrade_ops.ops:
        table_name = op_.table_name
        table_obj = target_metadata.tables.get(table_name)
        final_upgrade_ops.append(op_)

        # Create hypertable if configured
        hypertable_meta = getattr(table_obj, '__hypertable__', None)
        if hypertable_meta:
            upgrade, downgrade = create_hypertable_ops(
                table_name, hypertable_meta)
            final_upgrade_ops.extend(upgrade)
            final_downgrade_ops.extend(downgrade)

        # Create indexes if configured
        indexes_meta = getattr(table_obj, '__indexes__', None)
        if indexes_meta:
            upgrade, downgrade = create_index_ops(table_name, indexes_meta)
            final_upgrade_ops.extend(upgrade)
            final_downgrade_ops.extend(downgrade)

    # Update operations
    upgrade_ops.ops = final_upgrade_ops
    downgrade_ops.ops = final_downgrade_ops + downgrade_ops.ops
    


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        process_revision_directives=process_revision_directives,
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
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
