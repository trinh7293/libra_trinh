from app.tasks import query_page
from django.core.management.base import BaseCommand
import sys
import pika
from django.conf import settings



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('access_token', nargs='+', )

    def handle(self, **options):
        parameters = pika.connection.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()
        channel.queue_declare(queue='access_token_queue')
        access_token = str(options['access_token'][0])

        channel.basic_publish(exchange='',
                              routing_key='access_token_queue',
                              body=access_token,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        connection.close()
