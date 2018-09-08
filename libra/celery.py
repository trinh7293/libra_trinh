import os
import sys
import time
import pika
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libra.settings')

app = Celery('libra')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self, a, b):
    print('Request: {0!r}'.format(self.request))
    return a + b
