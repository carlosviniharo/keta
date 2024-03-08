#!/bin/bash

# Function to wait for PostgreSQL to be ready
wait_for_postgresql() {
    while ! nc -z db 5432; do
        echo "Waiting for PostgreSQL to be ready..."
        sleep 2
    done
}

# Function to initialize Django
initialize_django() {
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
}

# Wait for the Database to be ready
wait_for_postgresql

# Initialize Django
initialize_django

# Start Django
# Uncomment the appropriate line based on your preference
# apache2ctl -D FOREGROUND
# OR
python manage.py runserver 0.0.0.0:8000