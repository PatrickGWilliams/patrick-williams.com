FROM python:3

WORKDIR /

RUN mkdir -p /app/shared

WORKDIR /app

COPY patrickwilliamswebsite-1.4.1-py3-none-any.whl /app/

RUN pip install --no-cache-dir /app/patrickwilliamswebsite-1.4.1-py3-none-any.whl  && rm /app/patrickwilliamswebsite-1.4.1-py3-none-any.whl

COPY ./var /usr/local/var

EXPOSE 8041

CMD [ "waitress-serve", "--port=8041", "--call", "PatrickWilliamsWebsite:create_app" ]
