#!/bin/bash

set -e  # Exit immediately if a command fails

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || { echo "Error: Project directory not found!"; exit 1; }

VERSIONS_DIR="alembic/versions"

# Check if the versions directory exists and contains migration files
if [ ! -d "$VERSIONS_DIR" ] || ! find "$VERSIONS_DIR" -mindepth 1 | read; then
    echo "⚠️ No migration files found. Initializing Alembic migration..."
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    echo "Database initialized with first migration."
    exit 0
fi

echo "Checking for model changes..."
MIGRATION_OUTPUT=$(alembic revision --autogenerate -m "Auto migration" 2>&1)

# Check if Alembic detected changes
if echo "$MIGRATION_OUTPUT" | grep -q "No changes detected"; then
    echo "No changes detected. Skipping migration."
    exit 0
fi

# Extract the new migration file name
NEW_MIGRATION_FILE=$(echo "$MIGRATION_OUTPUT" | grep -oE "alembic/versions/[0-9a-f]+_.*\.py" | tail -n 1)

if [ -z "$NEW_MIGRATION_FILE" ]; then
    echo "No valid migration file found after autogenerate. Skipping upgrade."
    exit 1
fi

echo "Applying migration: $NEW_MIGRATION_FILE"
alembic upgrade head
echo "Migration applied successfully."
