from app.tasks import get_token, analyzer, push_to
from django.core.management.base import BaseCommand
from celery import chain


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('access_token', nargs='+', )

    def handle(self, **options):
        res = chain(get_token.s(10), analyzer.s(), push_to.s())()
        res.get()
        # get_token.delay(10)
