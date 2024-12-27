FROM python:slim

WORKDIR /app/data

WORKDIR /app

COPY docker/requirements.txt docker/boot.sh /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY flask/PatrickWilliamsWebsite/ /app/PatrickWilliamsWebsite/

COPY flask/words_alpha.txt  /app/

COPY flask/config.py /app/instance/config.py

COPY flask/migrations/ /app/migrations/

EXPOSE 8041

ENTRYPOINT ["./boot.sh"]
