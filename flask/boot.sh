#!/bin/bash
flask --app PatrickWilliamsWebsite db migrate
flask --app PatrickWilliamsWebsite db upgrade
exec waitress-serve --port=8041 --call PatrickWilliamsWebsite:create_app
