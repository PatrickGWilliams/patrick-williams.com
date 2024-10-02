FROM python:3

WORKDIR /

RUN mkdir -p /app/shared

WORKDIR /app

COPY patrickwilliamswebsite-1.3.4-py3-none-any.whl /app/

RUN pip install --no-cache-dir /app/patrickwilliamswebsite-1.3.4-py3-none-any.whl  

RUN rm /app/patrickwilliamswebsite-1.3.4-py3-none-any.whl

COPY ./var /usr/local/var

EXPOSE 8041

CMD [ "waitress-serve", "--port=8041", "--call", "PatrickWilliamsWebsite:create_app" ]
