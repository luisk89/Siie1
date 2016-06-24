#!/bin/bash

source /home/karatbars/.virtualenvs/karatbars/bin/activate
cd /home/karatbars/webapps/karatbars
exec python manage.py $1