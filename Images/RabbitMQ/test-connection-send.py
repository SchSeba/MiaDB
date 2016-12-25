from time import sleep

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               '192.168.139.254',5672))
channel = connection.channel()

channel.queue_declare(queue='hello')
count = 0
while True:
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World! ' + str(count))
    print(" [x] Sent 'Hello World!'")
    sleep(1)
    count+=1

connection.close()