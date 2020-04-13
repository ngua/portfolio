#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Postgres started"
fi

python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
    User.objects.create_superuser($SU_USERNAME, $SU_EMAIL, $SU_PASSWORD)" | python manage.py shell

exec "$@"
