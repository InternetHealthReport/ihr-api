# Database Migrations with Alembic and TimescaleDB

## 1. Creating a New Migration

Generate a new migration file based on changes detected in your SQLAlchemy models:

```bash
alembic revision --autogenerate -m "Describe your change"
```

* Alembic will generate a migration script reflecting structural changes.
* On first execution, an `alembic_version` table will be created to track migration history.

---

## 2. Previewing Migration SQL (Without Execution)

To inspect the SQL that Alembic would generate, without applying changes:

```bash
alembic upgrade head --sql
```

* Displays the SQL to upgrade to the latest revision.

```bash
alembic upgrade <revision_id> --sql
```

* Shows the SQL required to upgrade to a specific revision.

```bash
alembic upgrade <old_rev>:<new_rev> --sql
```

* Displays SQL for the changes between two specific revisions.

---

## 3. Applying Migrations

To apply all unapplied migrations:

```bash
alembic upgrade head
```

* Executes the latest migration and updates the database schema accordingly.

---

## 4. Downgrading the Schema

To revert the schema to a previous state:

```bash
alembic downgrade <revision_id>
```

* Rolls back the schema to the specified migration revision.

---

## 5. Safely Modifying Existing Tables

When adding new columns to tables with existing data:

* Make the column **nullable**, or
* Provide a **default value** during the migration

---

## 6. Preventing Unintended Drops

Control what Alembic includes in autogenerated migrations using the `include_object` hook in `/alembic/env.py`:

```python
def include_object(object, name, type_, reflected, compare_to):
    if reflected and compare_to is None:
        if type_ in ("table", "index"):
            return False
    return True
```

This prevents Alembic from generating DROP operations for:

* Tables and indexes that exist in the database
* But are not present in your SQLAlchemy models
---

# TimescaleDB Customizations

TimescaleDB adds powerful features for time-series workloads, such as **hypertables**, **compression**, and **retention policies**. These capabilities are not directly supported by SQLAlchemy or Alembic, so customization is required.

All TimescaleDB-specific logic is implemented in **`/alembic/env.py`** through several helper functions and hooks.

---

## Example SQLAlchemy Model

Below is an example SQLAlchemy model that uses TimescaleDB metadata:

```python
class HegemonyCone(Base):

    __indexes__ = [
        {
            'name': 'ihr_hegemonycone_asn_id_timebin_idx',
            'columns': ['asn_id', 'timebin DESC']
        },
    ]

    __hypertable__ = {
        'time_column': 'timebin',
        'chunk_time_interval': '2 day',
        'compress': True,
        'compress_segmentby': 'asn_id,af',
        'compress_orderby': 'timebin',
        'compress_policy': True,
        'compress_after': '7 days'
    }

    ...
```

This metadata drives the logic for custom hypertable creation, compression, and index generation.

---

## Key Functions in `/alembic/env.py`
All functions in `/alembic/env.py` are invoked automatically by alembic during the automatic generation of the migration file (we don't call them manually).

### 1. `process_revision_directives`

A hook that allows you to modify Alembic’s migration script before it's written:

```python
def process_revision_directives(context, revision, directives):
    if directives[0].upgrade_ops is not None:
        process_ops(
            context, directives[0].upgrade_ops, directives[0].downgrade_ops
        )
```

* Intercepts autogenerated operations.
* Passes them to `process_ops` for enhancement.

---

### 2. `process_ops`

This is the orchestrator for customizing TimescaleDB migrations:

```python
def process_ops(context, upgrade_ops, downgrade_ops):
    ...
```

* Iterates over all `CreateTableOp` operations.
* If a table has `__hypertable__` metadata:

  * Adds SQL to create a **hypertable**
  * Applies **compression settings** and **compression policy**
* If the model has `__indexes__`:

  * Adds **TimescaleDB-optimized indexes**
* Only applies hypertable logic when the table is first created. It does **not** support converting an existing table into a hypertable.

---

### 3. `create_hypertable_ops`

Handles hypertable creation and optional compression logic:

```python
def create_hypertable_ops(table_name, hypertable_meta, is_existing=False):
    ...
```

* Reads from the model’s `__hypertable__` metadata.
* Generates SQL for:

  * `SELECT create_hypertable(...)`
  * `ALTER TABLE ... SET(...)` for compression
  * `SELECT add_compression_policy(...)`

---

### 4. `create_index_ops`

Creates custom indexes defined in the model’s `__indexes__` attribute:

```python
def create_index_ops(table_name, indexes_meta):
    ...
```

* Parses index definitions
* Generates `CREATE INDEX IF NOT EXISTS ...`
* Adds reversible `DROP INDEX` for downgrade

---

### 5. `check_index_exists`

Prevents duplicate index creation by checking the PostgreSQL catalog:

```python
def check_index_exists(context, table_name, index_name):
    ...
```

* Queries `pg_indexes` to determine if an index already exists.

