FROM python

RUN pip install pika
RUN pip install redis
RUN pip install minio

WORKDIR /app

COPY *.py /app/
COPY transaction.json /app/

ENTRYPOINT [ "python3", "consumer.py" ]