from time import sleep

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.139.254', 5672))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    sleep(2.5)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()