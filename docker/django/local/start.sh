#! /usr/bin/bash
<<<<<<< HEAD
python manage.py collectstatic --noinput --settings=config.settings.local
=======
>>>>>>> d7e32345a1063484a09083d79a3333dc831b71d3
python manage.py migrate --settings=config.settings.local
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local