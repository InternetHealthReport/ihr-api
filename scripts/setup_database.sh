#!/bin/bash

# Load environment variables
DB_NAME=${DB_NAME:-"ihr_bash"}
DB_USER=${DB_USER:-"ihr_bash_user"}
DB_PASSWORD=${DB_PASSWORD:-"ihr_password"}
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-5434}
ADMIN_USER=${ADMIN_USER:-"django"}  # Superuser for setup

echo "Setting up PostgreSQL database..."

# Ensure PostgreSQL service is running
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" > /dev/null 2>&1; then
    echo "Error: PostgreSQL is not running on $DB_HOST:$DB_PORT"
    exit 1
fi

# Check if the database exists
DB_EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
if [ "$DB_EXISTS" != "1" ]; then
    echo "Creating database $DB_NAME..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\";" \
        && echo "Database $DB_NAME created."
else
    echo "Database $DB_NAME already exists."
fi

# Check if the user exists
USER_EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")
if [ "$USER_EXISTS" != "1" ]; then
    echo "Creating user $DB_USER..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "CREATE USER \"$DB_USER\" WITH PASSWORD '$DB_PASSWORD';" \
        && echo "User $DB_USER created."
else
    echo "User $DB_USER already exists."
fi

# Grant privileges
echo "Setting permissions..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"$DB_NAME\" TO \"$DB_USER\";"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "ALTER DATABASE \"$DB_NAME\" OWNER TO \"$DB_USER\";"

# Grant schema privileges inside the new database
psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO \"$DB_USER\";"

echo "Database setup completed."
