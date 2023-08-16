#! /usr/bin/bash
python manage.py collectstatic --noinput --settings=config.settings.local
python manage.py migrate --settings=config.settings.local
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local