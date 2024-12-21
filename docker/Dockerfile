FROM python:3


RUN mkdir -p /app/data 

WORKDIR /app

RUN mkdir /app/instance && pip install --no-cache-dir git+https://github.com/PatrickGWilliams/patrick-williams.com.git@alchemy#subdirectory=flask --target /app

COPY words_alpha.txt boot.sh /app/

COPY config.py /app/instance

COPY ./migrations/ /app/migrations/

RUN chmod a+x boot.sh

EXPOSE 8041

ENTRYPOINT ["./boot.sh"]
