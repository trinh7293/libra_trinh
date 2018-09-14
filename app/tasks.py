import pika
import sys
import time
from libra.celery import app
from app.libs.facebook import FacebookClient
from django.conf import settings


@app.task(bind=True)
def query_page(self, page_id):
    # parameters = pika.ConnectionParameters(host='localhost')
    parameters = pika.connection.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel_error = connection.channel()
    channel.queue_declare(queue=settings.ACCESS_TOKEN_QUEUE)
    channel_error.queue_declare(
        queue=settings.ACCESS_TOKEN_ERROR_QUEUE)
    access_token = None
    while True:
        print('start_while')
        method_frame, header_frame, body = channel.basic_get(
            settings.ACCESS_TOKEN_QUEUE)
        if method_frame is None:
            print('No message returned')
            access_token = None
            break
        access_token_from_queue = body.decode("utf-8")
        try:  # check access token
            client_check = FacebookClient(
                access_token_from_queue, settings.VERSION_1_0)
            client_check.fetch_obj(page_id)
            access_token = access_token_from_queue
            channel.basic_ack(method_frame.delivery_tag)
            channel.basic_publish(
                exchange='',
                routing_key=settings.ACCESS_TOKEN_QUEUE,
                body=access_token_from_queue)
            break
        except Exception:  # handle invalid access token
            access_token = None
            channel.basic_ack(method_frame.delivery_tag)
            channel_error.basic_publish(
                exchange='',
                routing_key=settings.ACCESS_TOKEN_ERROR_QUEUE,
                body=access_token_from_queue)
        time.sleep(0.01)
    posts = None
    if access_token is not None:
        client = FacebookClient(access_token, settings.VERSION_1_0)
        posts = client.fetch_obj(page_id, 'posts')['data']
    return posts
