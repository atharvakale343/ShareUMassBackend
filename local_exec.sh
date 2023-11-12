#!/bin/bash

python3 manage.py makemigrations user image postings
python3 manage.py migrate
python3 manage.py migrate --database=images
python3 manage.py runserver 0.0.0.0:80
