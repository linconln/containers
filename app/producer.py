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

print("Finalizado")