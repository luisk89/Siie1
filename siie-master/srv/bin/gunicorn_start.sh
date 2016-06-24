#!/bin/bash

source /home/karatbars/.virtualenvs/karatbars/bin/activate
cd /home/karatbars/webapps/karatbars
gunicorn --env DJANGO_SETTINGS_MODULE=karatbarslatinoamericano.settings karatbarslatinoamericano.wsgi:application --config srv/conf/gunicorn_conf.py

