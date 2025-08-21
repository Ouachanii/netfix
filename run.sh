#!/usr/bin/env bash
set -e  # exit on error

# go into project
cd "$(dirname "$0")/"

# create venv if missing
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# activate
source .venv/bin/activate

# install deps
pip install -q "Django==3.1.14"

# migrate
python3 manage.py makemigrations
python3 manage.py migrate

# optional: create superuser if DB is fresh
if ! python3 manage.py shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)"; then
    echo "No admin user found. Creating one..."
    python3 manage.py createsuperuser
fi

# run server
python3 manage.py runserver

