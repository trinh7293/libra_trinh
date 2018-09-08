from django.core.management.base import BaseCommand
import pika
from app.tasks import query_page
# from django.conf import settings
# parameters = pika.connection.URLParameters(settings.RABBITMQ_URL)
# connection = pika.BlockingConnection(parameters=parameters)


class Command(BaseCommand):
    def handle(self, **options):
        query_page.delay('me')
