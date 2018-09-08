from django.core.management.base import BaseCommand
import pika
from django.conf import settings
parameters = pika.connection.URLParameters(settings.RABBITMQ_URL)
connection = pika.BlockingConnection(parameters=parameters)


class Command(BaseCommand):
    def handle(self, **options):
        channel = connection.channel()
        res = channel.queue_declare(queue='access_token_queue')
        count = res.method.message_count
        print(res)
        print(count)
