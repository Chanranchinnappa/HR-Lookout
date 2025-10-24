# =============================================================================
# Database Migration Script (Windows PowerShell)
# =============================================================================

Write-Host "Starting database migrations..." -ForegroundColor Cyan

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run migrations
Write-Host "Running Django migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host "Migrations complete!" -ForegroundColor Green
