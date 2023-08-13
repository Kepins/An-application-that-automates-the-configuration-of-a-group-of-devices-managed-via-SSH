#! /usr/bin/bash
python manage.py migrate --settings=config.settings.production
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.production