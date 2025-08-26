## 1. Create the target database

First, create the target database `ihr-fastapi` where you want the tables and data to reside:


## 2. Run Alembic migrations

Run Alembic to create the schema and tables inside `ihr-fastapi`:

```bash
alembic upgrade head
```

This ensures the target database has all the required tables ready.

---

## 3. Connect to `ihr-fastapi` using psql

Open a `psql` session to your target database:

```bash
psql -U <USERNAME> -d ihr-fastapi
```

Replace `<USERNAME>` with your PostgreSQL username.

---
## 4. Configure FDW to access the source database (`ihr`)

Inside the `psql` session, run:

```sql
-- Enable the FDW extension
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- Create a connection to the ihr DB
CREATE SERVER "<SERVER_NAME>"
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host '<HOST>', dbname '<DB_NAME>', port '<PORT>');

-- Map your Postgres user to the remote DB credentials
CREATE USER MAPPING FOR CURRENT_USER
SERVER "<SERVER_NAME>"
OPTIONS (user '<USERNAME>', password '<PASSWORD>');

-- Import only the needed tables into a schema called ihr_src
CREATE SCHEMA IF NOT EXISTS ihr_src;
IMPORT FOREIGN SCHEMA public
FROM SERVER "<SERVER_NAME>"
INTO ihr_src;
```

Replace the following placeholders with your actual values:
- `<SERVER_NAME>`: A name for your foreign server 
- `<HOST>`: The hostname where your source database is running 
- `<DB_NAME>`: The name of your source database 
- `<PORT>`: The PostgreSQL port 
- `<USERNAME>`: Your PostgreSQL username for the source database
- `<PASSWORD>`: Your PostgreSQL password for the source database

### Explanation

* **`CREATE EXTENSION`** enables FDW support.
* **`CREATE SERVER`** defines the connection to the source DB (`ihr`).
* **`USER MAPPING`** maps your local PostgreSQL user to the remote DB user/password.
* **`IMPORT FOREIGN SCHEMA`** pulls in table definitions into a local schema (`ihr_src`). These are **foreign tables** that point to the source DB.

---

## 5. Prepare to export migration SQL

We’ll generate a file (`migration.sql`) with `INSERT ... SELECT` statements to copy the data.

In `psql`, run:

```sql
\x off
\pset format unaligned
\pset pager off
\pset tuples_only on
\o migration.sql
```

### Explanation

* **`\x off`** → disables expanded display.
* **`\pset format unaligned`** → outputs raw SQL without table formatting.
* **`\pset pager off`** → prevents paging.
* **`\pset tuples_only on`** → suppresses headers/footers.
* **`\o migration.sql`** → redirects all output into a file named `migration.sql`.

---

## 6. Generate the data migration SQL

Run this query in `psql`:

```sql
SELECT 
    'INSERT INTO public.' || table_name || ' (' ||
    string_agg(column_name, ', ' ORDER BY ordinal_position) ||
    ') SELECT ' ||
    string_agg(column_name, ', ' ORDER BY ordinal_position) ||
    ' FROM ihr_src.' || table_name ||
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.columns c2
            WHERE c2.table_schema = 'public' 
            AND c2.table_name = c.table_name 
            AND c2.column_name = 'timebin'
        ) 
        THEN ' WHERE timebin >= NOW() - INTERVAL ''3 months'';'
        ELSE ';'
    END ||
    E'\n' ||
    '\echo ''SUCCESS: ' || table_name || ' data inserted'''
FROM information_schema.columns c
WHERE table_schema = 'public' 
AND table_name LIKE 'ihr_%'
GROUP BY table_name
ORDER BY table_name;
```

This builds a series of `INSERT INTO ... SELECT ...` statements that:

* Copy all data from `ihr_src.table` to `public.table`.
* If a `timebin` column exists, only copy rows from the **last 3 months**.
* Print a confirmation message (`SUCCESS: ...`) after each table insert.

---

## 7. Exit `psql`

Type:

```sql
\q
```

Now you’ll have a file called `migration.sql` in your current directory.

---

## 8. Run the migration

Finally, execute the migration script against the `ihr-fastapi` database:

```bash
psql -U <USERNAME> -d ihr-fastapi -f migration.sql
```

This will insert data into all your new tables.
