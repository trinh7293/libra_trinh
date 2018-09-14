from django.core.management.base import BaseCommand
import pika
from app.tasks import query_page


class Command(BaseCommand):
    def handle(self, **options):
        query_page.delay('me')
