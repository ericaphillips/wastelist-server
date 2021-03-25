#!/bin/bash
rm -rf wastelistapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations wastelistapi
python3 manage.py migrate wastelistapi
python3 manage.py loaddata user
python3 manage.py loaddata token
python3 manage.py loaddata pharmacy
python3 manage.py loaddata wasteuser
python3 manage.py loaddata messages