FROM python:slim

WORKDIR /app/data

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./PatrickWilliamsWebsite/ /app/PatrickWilliamsWebsite/

COPY words_alpha.txt boot.sh /app/

COPY config.py /app/instance/config.py

COPY ./migrations/ /app/migrations/

EXPOSE 8041

ENTRYPOINT ["./boot.sh"]
