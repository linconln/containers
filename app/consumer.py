import pika
import json
import redis

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = "rabbit",
    port = 5672,
    virtual_host = "/"
))

channel = connection.channel()

queue_name = "fraud_validator_queue"

channel.queue_declare(queue="fraud_validator_queue")
channel.queue_bind(exchange="amq.fanout", queue="fraud_validator_queue")

cache = redis.Redis(host='redis', port=6379, db=0)

def chamado_quando_uma_transacao_eh_consumida(channel, method_frame, header_frame, body):
    transaction = json.loads(body.decode('utf-8'))
    chave = transaction["conta"]
    fraude = 0
    media_lida = cache.lindex(chave, 0)
    if(media_lida==None):
        media = transaction["value"]
        cache.rpush(chave, media)
    else:
        desvio = transaction["value"] / float(media_lida)
        if(desvio > 1.4):
            print("Fraude: ", transaction)
            fraude = 1
            cache.rpush("report-"+str(chave), "Fraude: "+json.dumps(transaction))
        soma = 0
        contador = 0
        res = cache.lrange(chave, 1, 9999)
        for x in res:
            y = json.loads(x)
            if(fraude==1):
                cache.rpush("report-"+str(chave), "Histórico: "+str(x))
            contador = contador + 1
            soma = soma + y["value"]
        contador = contador + 1
        soma = soma + transaction["value"]
        media = soma / contador
        cache.lset(chave, 0, media)

    cache.rpush(chave, json.dumps(transaction))
    
channel.basic_consume(queue=queue_name,
                      on_message_callback=chamado_quando_uma_transacao_eh_consumida, auto_ack=True)

print("Esperando por mensagens. Para sair pressione CTRL+C")
channel.start_consuming()