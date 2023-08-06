import os
import pika
from pika import PlainCredentials
from dotenv import load_dotenv

from hautils.logger import logger

load_dotenv(override=False)

RABBIT_MQ_HOST = os.getenv('RABBIT_MQ_HOST')
RABBIT_MQ_USER = os.getenv("RABBIT_MQ_USER")
RABBIT_MQ_PASS = os.getenv("RABBIT_MQ_PASS")


def get_rmq_connection():
    logger.info("connecting to rmq %s - %s - %s" % (RABBIT_MQ_HOST, RABBIT_MQ_USER, RABBIT_MQ_PASS))
    return pika.BlockingConnection(
        pika.ConnectionParameters(heartbeat=1000, host=RABBIT_MQ_HOST,
                                  credentials=PlainCredentials
                                  (RABBIT_MQ_USER, RABBIT_MQ_PASS)))


def publish_rmq(exchange, body, ex_type="direct"):
    connection = get_rmq_connection()
    channel = connection.channel()
    logger.info("publishing to exchange %s with data %s" % (exchange, body))
    channel.exchange_declare(exchange=exchange, exchange_type=ex_type)
    channel.basic_publish(exchange=exchange, routing_key=exchange, body=body)
    connection.close()
    logger.info("closing connection")


def rmq_bind(exchange="ha", queue="ha"):
    logger.info("binding queues together %s to %s" % (exchange, queue))
    connection = get_rmq_connection()
    channel = connection.channel()
    result = channel.queue_declare(queue=queue, exclusive=False, durable=True)
    logger.info("queue declare result %s" % (result,))
    result = channel.queue_bind(exchange=exchange,
                                queue=queue, routing_key=exchange)
    logger.info("queue bind result %s" % (result,))
    return channel


def rmq_consume(queue, callback, durable=True, ack=True):
    logger.info("rmq consumer getting ready")
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=durable)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=ack)
    logger.info("consumer bound to %s " % (queue,))
    return channel
