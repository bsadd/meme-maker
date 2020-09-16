#!/bin/sh

python manage.py makemigrations accounts coreapp
python manage.py migrate

python manage.py collectstatic --no-input
