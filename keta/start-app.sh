#!/bin/bash

# Function to wait for PostgreSQL to be ready.
wait_for_postgresql() {
    while ! nc -z db 5432; do
        echo "Waiting for PostgreSQL to be ready..."
        sleep 2
    done
}

# Function to initialize Django.
initialize_django() {
    /venv/bin/python manage.py makemigrations
    /venv/bin/python manage.py migrate
    /venv/bin/python manage.py collectstatic --noinput
}

# Wait for the Database to be ready.
#wait_for_postgresql

# Start cron service in the background
service cron start

# Initialize Django
initialize_django

# Start Django
# Uncomment the appropriate line based on your preference.
source /venv/bin/activate
apache2ctl -D FOREGROUND
# OR
# python management.py runserver 0.0.0.0:8000