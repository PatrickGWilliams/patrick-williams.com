FROM python:3

RUN mkdir /data && pip install --no-cache-dir git+https://github.com/PatrickGWilliams/patrick-williams.com.git@alchemy#subdirectory=flask

COPY ./var /usr/local/var

EXPOSE 8041

CMD [ "waitress-serve", "--port=8041", "--call", "PatrickWilliamsWebsite:create_app" ]
