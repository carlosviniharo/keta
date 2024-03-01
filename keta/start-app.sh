## Wait for the Database to be ready
while ! nc -z db 5432; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

# Initialize Django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Start Django
#apache2ctl -D FOREGROUND
python manage.py runserver 0.0.0.0:8000