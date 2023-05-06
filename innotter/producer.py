import os

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq_innotter"
    )
)
channel = connection.channel()
channel.queue_declare(queue='page-statistics')


def publish(method: str, body: dict[str, str]) -> None:
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='page-statistics', body=body, properties=properties
    )
