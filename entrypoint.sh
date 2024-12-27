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

# Function to check if a table is empty
function is_table_empty() {
  TABLE_NAME=$1
  RESULT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM $TABLE_NAME;")
  if [ "$RESULT" -eq "0" ]; then
    return 0  # Empty
  else
    return 1  # Not empty
  fi
}

# Populate the neighbourhood table if empty
if is_table_empty "neighborhood"; then
  echo "Populating 'neighborhood' table..."
  python data_source/populate_neighbourhood.py
else
  echo "'neighborhood' table already populated."
fi

# Populate the listings and room tables if empty
if is_table_empty "listings"; then
  echo "Populating 'listings' and 'room' tables..."
  python data_source/populate_listing_and_room.py
else
  echo "'listings' table already populated."
fi

# Start the FastAPI app with Uvicorn
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload