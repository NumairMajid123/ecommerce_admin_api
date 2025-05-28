#!/bin/bash

# Exit on error
set -e

echo "Setting up database..."

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create demo data
echo "Creating demo data..."
python scripts/init_db.py

echo "Database setup complete!" 