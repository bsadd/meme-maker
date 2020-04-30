bash resetmigrations.sh
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json -e contenttypes -e auth
