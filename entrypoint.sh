#!/bin/sh

echo "Waiting for PostgreSQL..."

echo "Waiting for PostgreSQL..."
until python -c "import socket; s = socket.socket(); s.connect(('db', 5432))"; do
  sleep 1
done

echo "PostgreSQL is up - continuing..."

echo "PostgreSQL started"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn easyux.wsgi:application --bind 0.0.0.0:8000

python manage.py migrate
exec "$@"