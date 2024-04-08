# Le o arquivo json e envia para o serviço de mensageria

import datetime
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = "rabbit",
    port = 5672,
    virtual_host = "/"
))

channel = connection.channel()

transaction_file = open("transaction.json")

transactions = json.load(transaction_file)

transaction_file.close()

for transaction in transactions:
    transaction["data"] = str(datetime.datetime.now())
    channel.basic_publish(exchange="amq.fanout",
                          routing_key="",
                          body=json.dumps(transaction)
                          )

# verifica o cache, calcula a media, gera relatório no Min-IO quando encontra a condição de fraude e depois mostra os endereços para download dos relatórios

from minio import Minio
import redis
import io
import os

SERVER = os.getenv("SERVER_NAME")
cliente = Minio(
    endpoint=f"{SERVER}:9000",
    access_key="minioadmin", 
    secret_key="minioadmin",
    secure=False)

bucket_name = "bucket"
if cliente.bucket_exists(bucket_name):
    print("Bucket existe!")
else:
    cliente.make_bucket(bucket_name)

cache = redis.Redis(host='redis', port=6379, db=0)

chaves = cache.keys("report*")

for chave in chaves:
    str_chave = chave.decode("utf-8")
    str_chave = str_chave+".txt"
    reports = cache.lrange(chave, 0, 999999)
    value=""
    size=0
    for report in reports:
        str_report=report.decode("utf-8")
        value=value+str_report+"\n"

    size=len(value)
    value_as_bytes=value.encode("utf-8")
    str_reports=io.BytesIO(value_as_bytes)

    result = cliente.put_object(
        bucket_name=bucket_name,
        object_name=str_chave,
        data=str_reports,
        length=size
    )

    get_url = cliente.get_presigned_url(
        method='GET',
        bucket_name=bucket_name,
        object_name= str_chave, )

    print(f"Download URL: [GET] {get_url}")