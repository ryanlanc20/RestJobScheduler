import pika
import json

def submit_notification(notification):
    # TODO: Create connection manager class return connection object.
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="notifications-queue"))
        channel = connection.channel()
        channel.queue_declare(queue="notifications")

        channel.basic_publish(exchange="",routing_key="notifications",body=json.dumps(notification))
        connection.close()
        return True
    except:
        return False