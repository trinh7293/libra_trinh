from libra.celery import app
from app.libs.facebook import FacebookClient
from django.conf import settings
import pika
import sys
import time
# pika.ConnectionParameters(host='localhost')

ACCESS_TOKEN_QUEUE = settings.ACCESS_TOKEN_QUEUE
ACCESS_TOKEN_ERROR_QUEUE = settings.ACCESS_TOKEN_ERROR_QUEUE


@app.task(bind=True)
def query_page(self, page_id):
    parameters = pika.connection.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel_error = connection.channel()
    channel.queue_declare(queue=ACCESS_TOKEN_QUEUE)
    channel_error.queue_declare(
        queue=ACCESS_TOKEN_ERROR_QUEUE)
    # q = Query_page(connection, page_id)
    access_token = None
    while True:
        print('start_while')
        method_frame, header_frame, body = channel.basic_get(
            ACCESS_TOKEN_QUEUE)
        if method_frame:
            # print(method_frame, header_frame, body)
            channel.basic_ack(method_frame.delivery_tag)
        else:
            print('No message returned')
            access_token = None
            break
        access_token_from_queue = body.decode("utf-8")
        try:  # check access token
            client_check = FacebookClient(
                access_token_from_queue, settings.VERSION_1_0)
            client_check.fetch_obj(page_id)
            access_token = access_token_from_queue
            channel.basic_publish(
                exchange='',
                routing_key=ACCESS_TOKEN_QUEUE,
                body=access_token_from_queue)
            break
        except Exception:  # handle invalid access token
            access_token = None
            channel_error.basic_publish(
                exchange='',
                routing_key=ACCESS_TOKEN_ERROR_QUEUE,
                body=access_token_from_queue)
        time.sleep(0.01)
    posts = None
    if access_token != None:
        client = FacebookClient(access_token, settings.VERSION_1_0)
        posts = client.fetch_obj(page_id, 'posts')['data']
    return posts


@app.task(bind=True)
def get_token(self, page_id):
    return page_id


@app.task(bind=True)
def analyzer(self, page_get):
    return page_get + 3


@app.task(bind=True)
def push_to(self, page_ana):
    return page_ana + 4
