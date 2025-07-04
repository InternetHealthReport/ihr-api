import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.database import Base
import importlib.util
import pathlib
from alembic.operations import ops
from alembic.operations.ops import CreateIndexOp
from sqlalchemy import inspect, text
from dotenv import load_dotenv


# Get Alembic config
config = context.config

# Load environment variables from .env file
try:
    load_dotenv()
except:
    pass
# Override Alembic DB URL (found in alembic.ini) with the DB URL found in the .env file
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- DYNAMIC MODEL DISCOVERY ---

# Add models directory to the path
models_path = pathlib.Path(__file__).parent.parent / "models"
sys.path.append(str(models_path.parent))

model_classes = []

# Load all model classes inheriting from Base (excluding __init__.py)
# This is done so that we can later access __hypertable__ and __indexes__ attributes defined in the models and use them in generating the SQL commands
for file in models_path.glob("*.py"):
    if file.name != "__init__.py":
        module_name = f"models.{file.stem}"
        module = importlib.import_module(module_name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Base) and attr != Base:
                model_classes.append(attr)


# Set Alembic's metadata target for autogeneration
target_metadata = Base.metadata

# Attach custom metadata (hypertable and indexes) to the tables
for model in model_classes:
    table = target_metadata.tables.get(model.__tablename__)
    if table is not None:
        # Associate hypertable metadata
        if hasattr(model, '__hypertable__'):
            setattr(table, '__hypertable__', model.__hypertable__)

        # Associate indexes metadata
        if hasattr(model, '__indexes__'):
            setattr(table, '__indexes__', model.__indexes__)


# --- MIGRATION BEHAVIOR CUSTOMIZATION ---


def include_object(object, name, type_, reflected, compare_to):
    # Prevent dropping tables and indexes that are found in database and aren't found in the models
    if reflected and compare_to is None:
        if type_ in ("table", "index"):
            return False
    return True


def process_revision_directives(context, revision, directives):
    """
    Hook to modify the autogenerated alembic migration file before it's generated.
    Injects hypertable and index creation SQL.
    """
    if directives[0].upgrade_ops is not None:
        process_ops(
            context,  directives[0].upgrade_ops, directives[0].downgrade_ops)


# --- HELPERS FOR HYPERTABLES AND INDEXES ---

def create_hypertable_ops(table_name, hypertable_meta, is_existing=False):
    """
    Generate SQL operations for TimescaleDB hypertable creation and compression.
    """
    upgrade_ops = []
    downgrade_ops = []

    time_col = hypertable_meta['time_column']
    chunk_interval = hypertable_meta.get('chunk_time_interval', '1 day')

    # Create hypertable SQL
    hypertable_sql = (
        f"SELECT create_hypertable('{table_name}', by_range('{time_col}', INTERVAL '{chunk_interval}'));"
    )

    upgrade_ops.append(ops.ExecuteSQLOp(hypertable_sql))

    # Handle compression settings
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
    """
    Generate SQL operations for index creation and deletion.
    """
    upgrade_ops = []
    downgrade_ops = []

    for idx in indexes_meta:
        col_list = ', '.join(idx['columns'])
        create_index_sql = f"CREATE INDEX IF NOT EXISTS {idx['name']} ON {table_name} ({col_list});"
        upgrade_ops.append(ops.ExecuteSQLOp(create_index_sql))

        drop_index_sql = f"DROP INDEX IF EXISTS {idx['name']};"
        downgrade_ops.append(ops.ExecuteSQLOp(drop_index_sql))

    return upgrade_ops, downgrade_ops


def check_index_exists(context, table_name, index_name):
    """
    Query PostgreSQL system tables to determine if an index already exists.
    This prevents Alembic from generating duplicate index statements.
    """
    print(index_name)
    # In offline mode, assume index doesn't exist
    if not hasattr(context, 'bind'):
        return False

    sql = text("""
    SELECT EXISTS (
        SELECT 1 
        FROM pg_indexes 
        WHERE tablename = :table_name 
        AND indexname = :index_name
    );
    """)

    try:
        return context.bind.execute(sql, {
            'table_name': table_name,
            'index_name': index_name
        }).scalar()
    except Exception:
        return False


def process_ops(context, upgrade_ops, downgrade_ops):
    """
    Inject hypertable and index-related SQL into Alembic upgrade/downgrade steps.
    """
    final_upgrade_ops = []
    new_downgrade_ops = []

    # Get all table names from metadata
    all_tables = target_metadata.tables.keys()

    # Handle table creations and their features
    for op_ in upgrade_ops.ops:
        table_name = op_.table_name
        table_obj = target_metadata.tables.get(table_name)

        # Always add table creation
        final_upgrade_ops.append(op_)

        # Only process hypertable ops if this is a table creation
        if isinstance(op_, ops.CreateTableOp):
            hypertable_meta = getattr(table_obj, '__hypertable__', None)
            if hypertable_meta:
                upgrade, downgrade = create_hypertable_ops(
                    table_name, hypertable_meta)
                final_upgrade_ops.extend(upgrade)
                new_downgrade_ops.extend(downgrade)

    # Handle index creations
    for table_name in all_tables:
        table_obj = target_metadata.tables.get(table_name)
        indexes_meta = getattr(table_obj, '__indexes__', None)

        if indexes_meta:
            new_indexes = [
                idx for idx in indexes_meta
                if not check_index_exists(context, table_name, idx['name'])
            ]
            if new_indexes:
                upgrade, downgrade = create_index_ops(
                    table_name, new_indexes)
                final_upgrade_ops.extend(upgrade)
                new_downgrade_ops.extend(downgrade)

    # Update operations
    upgrade_ops.ops = final_upgrade_ops
    downgrade_ops.ops = new_downgrade_ops + downgrade_ops.ops


# --- OFFLINE/ONLINE MIGRATION EXECUTION ---

def run_migrations_offline() -> None:
    """
    Run migrations without connecting to a database.
    """
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
    """
    Run migrations in online mode (connected to the database).
    """
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

# Execute appropriate migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
