import time
import json
import logging

import pika
import pika.exceptions

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging
logger = logger.getLogger(__name__)

SLEEP_RABBITMQ_QUEUE_OVERFLOW = 10
RABBITMQ_MAX_QUEUE_LENGTH = 30


class RBMQChannel:
    def __init__(self, auth: dict, queue_name: str = 'test', queue_settings: dict = None):
        self.auth = auth
        self.queue_name = queue_name
        self.queue_settings = queue_settings
        logger.info(f'RabbitMQ Server: {self.auth.get("host")} queue {self.queue_name}')
        self.res = None
        self.connection = None
        self.channel = None
        self.establish_connection()

    def __connect(self):
        try:
            credentials = pika.PlainCredentials(self.auth['username'], self.auth['password'])
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.auth['host'], port=self.auth['port'],
                                          heartbeat=1000,
                                          blocked_connection_timeout=600,
                                          virtual_host=self.auth['vhost'],
                                          credentials=credentials))
            self.channel = self.connection.channel()
            self.res = self.channel.queue_declare(
                queue=self.queue_name,
                durable=True,
                arguments=self.queue_settings
            )
            return True
        except pika.exceptions.ConnectionClosed:
            self.connection = None
            self.channel = None
            return False

    def count(self):
        if self.res:
            return self.res.method.message_count

    def basic_get_count(self, queue=None):
        if queue is None:
            queue = self.queue_name

        method_frame, properties, body = self.channel.basic_get(queue=queue)
        if method_frame is None:
            return 0
        count = method_frame.message_count + 1
        self.channel.basic_nack(delivery_tag=method_frame.delivery_tag)
        return count

    def establish_connection(self):
        self.connection = None
        self.channel = None

        while not self.connection:
            if self.__connect():
                break
            else:
                time.sleep(self.auth['reconnect_timeout'])

    def get_event(self):
        try:
            method_frame, _, body = self.channel.basic_get(self.queue_name)
        except (pika.exceptions.ChannelClosed, pika.exceptions.ConnectionClosed):
            self.establish_connection()
            method_frame, _, body = self.channel.basic_get(self.queue_name)

        if method_frame:
            event = json.loads(body.decode('utf-8', 'ignore'))
            return event, method_frame
        return None, None

    def publish_message(self, message):
        logger.debug(f'start publidh message {message}')
        try:
            body = message
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=body,  # message
                                       properties=pika.BasicProperties(
                                           content_type='text/plain',
                                           delivery_mode=2),
                                       mandatory=True)
        except pika.exceptions.UnroutableError:
            pass
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelWrongStateError):
            self.establish_connection()
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

    def delete_queue(self):
        self.channel.queue_delete(queue=self.queue_name)

    def close_connection(self):
        if self.connection and self.connection.is_closed is False:
            self.connection.close()

    def check_overflow_queue(self, queue=None, max_length=None):
        queue = queue or self.queue_name

        if max_length is None:
            if self.queue_settings and self.queue_settings.get('x-max-length'):
                max_length = self.queue_settings.get('x-max-length') / 2
            else:
                max_length = RABBITMQ_MAX_QUEUE_LENGTH

        while True:
            queue_length = self.basic_get_count(queue)
            if queue_length < max_length:
                break
            else:
                log_message = f"Queue overflow: {queue} max_length: {max_length}, current length: {queue_length}"

            logger.warning(f"{log_message}, Sleep {SLEEP_RABBITMQ_QUEUE_OVERFLOW} sec")
            time.sleep(SLEEP_RABBITMQ_QUEUE_OVERFLOW)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def __call__(self, *args, **kwargs):
        return self.channel
