FROM python:3


RUN mkdir -p /app/data && pip install --no-cache-dir git+https://github.com/PatrickGWilliams/patrick-williams.com.git@alchemy#subdirectory=flask --target /app

COPY config.py words_alpha.txt /app/

COPY migrations /app

COPY ./boot.sh ./
RUN chmod a+x boot.sh

EXPOSE 8041

ENTRYPOINT ["./boot.sh"]
