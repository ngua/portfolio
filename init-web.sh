#!/bin/sh

python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
    User.objects.create_superuser($SU_USERNAME, $SU_EMAIL, $SU_PASSWORD)" | python manage.py shell
python manage.py runserver 0.0.0.0:8000

