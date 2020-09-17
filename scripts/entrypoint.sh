#!/bin/sh

python manage.py collectstatic --no-input

python manage.py makemigrations
python manage.py migrate
    
#uwsgi --http :8000 --module=mememaker.wsgi:application --env DJANGO_SETTINGS_MODULE=mememaker.settings --master --enable-threads --wsgi-file mememaker/wsgi.py

uwsgi --ini uwsgi.ini
