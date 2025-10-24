#!/bin/bash
# =============================================================================
# Database Migration Script
# =============================================================================

echo "Starting database migrations..."

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Run migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if doesn't exist
echo "Creating superuser (if not exists)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hrlookout.local', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Migrations complete!"
