from django.core.management.base import BaseCommand
import pika
from app.tasks import query_page


class Command(BaseCommand):
    def handle(self, **options):
        test_page_id = '340332152808581'
        # test_me_node = 'me' 
        query_page.delay(test_page_id)
