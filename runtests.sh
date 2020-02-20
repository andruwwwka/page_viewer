while ! nc -z db 5432; do sleep 1; done;
python manage.py test --keepdb
