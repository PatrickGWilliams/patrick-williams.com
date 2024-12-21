#!/bin/bash
python3 -m flask --app PatrickWilliamsWebsite db migrate
python3 -m flask --app PatrickWilliamsWebsite db upgrade
exec python3 -m waitress --port=8041 --call PatrickWilliamsWebsite:create_app
