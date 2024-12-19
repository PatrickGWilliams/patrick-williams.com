#!/bin/bash
flask db migrate
flask db upgrade
exec waitress-serve --port=8041 --call PatrickWilliamsWebsite:create_app
