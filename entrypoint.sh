#!/bin/bash
# Exit immediately if a command exits with a non-zero status

set -e

# Function to check if the database is ready
function wait_for_db() {
  echo "Waiting for PostgreSQL to be ready..."
  until psql "$DATABASE_URL" -c '\q' 2>/dev/null; do
    >&2 echo "PostgreSQL is unavailable - sleeping"
    sleep 1
  done
  echo "PostgreSQL is up - continuing..."
}

# Run the function
wait_for_db

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head