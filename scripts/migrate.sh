#!/bin/bash
# Database migration script

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

echo "Migration completed!"
