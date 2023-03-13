import pika
import json

def submit_notification(notification):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="notifications_queue"))
        channel = connection.channel()
        channel.queue_declare(queue="notifications")

        channel.basic_publish(exchange="",routing_key="notifications",body=json.dumps(notification))
        connection.close()
        return True
    except:
        return False