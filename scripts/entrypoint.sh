#!/bin/sh


#uwsgi --http :8000 --module=mememaker.wsgi:application --env DJANGO_SETTINGS_MODULE=mememaker.settings --master --enable-threads --wsgi-file mememaker/wsgi.py

uwsgi --ini uwsgi.ini
