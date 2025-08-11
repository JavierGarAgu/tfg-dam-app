#!/bin/sh

set -e

host="$POSTGRES_HOST"
port="$POSTGRES_PORT"
db="$POSTGRES_DB"
user="$POSTGRES_USER"
password="$POSTGRES_PASSWORD"

echo "Esperando a que la base de datos '$db' esté disponible en $host:$port"

until python -c "import psycopg2; psycopg2.connect(
    dbname='$db', user='$user', password='$password', host='$host', port=$port)" >/dev/null 2>&1; do
    echo "La base de datos aún no está lista. Esperando"
    sleep 1
done

echo "La base de datos está lista. Aplicando migraciones"

#python manage.py makemigrations app

echo "Levantando Gunicorn"
export DJANGO_SETTINGS_MODULE=app.settings
exec gunicorn app.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4
