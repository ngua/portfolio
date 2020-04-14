#!/bin/sh

export PYTHONPATH=$(pwd)
python manage.py flush --no-input --settings=settings.dev
python manage.py makemigrations --no-input --settings=settings.dev
python manage.py migrate --settings=settings.dev
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
    User.objects.create_superuser($SU_USERNAME, $SU_EMAIL, $SU_PASSWORD)" | python manage.py shell --settings=settings.dev
python manage.py runserver 0.0.0.0:8000 --settings=$DJANGO_SETTINGS_MODULE
