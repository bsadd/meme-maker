#!/bin/sh

python manage.py makemigrations accounts coreapp
python manage.py migrate

python manage.py collectstatic --no-input


#uwsgi --http :8000 --module=mememaker.wsgi:application --env DJANGO_SETTINGS_MODULE=mememaker.settings --master --enable-threads --wsgi-file mememaker/wsgi.py

uwsgi --ini uwsgi.ini