import os

import pika

from microservice.db import PageStatisticsDatabase
from microservice.models import PageStatistics

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq_innotter"
    )
)

channel = connection.channel()
channel.queue_declare(queue="page-statistics")


def callback(ch, method, properties, body) -> None:
    page_statistics = PageStatistics.parse_raw(body)
    if properties.content_type == "create_page":
        PageStatisticsDatabase.create_item(page_statistics)
    elif properties.content_type == "update_page":
        PageStatisticsDatabase.update_item(page_statistics)
    elif properties.content_type == "delete_page":
        PageStatisticsDatabase.delete_item(page_statistics)


channel.basic_consume(queue="page-statistics", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
