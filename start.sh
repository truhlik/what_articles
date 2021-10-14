#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn articles.wsgi -b 0.0.0.0:8000 --workers=4 --timeout 300
