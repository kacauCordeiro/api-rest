import os
import pika

class Rabbitmq:
    
    def __init__(self, ):
        """Construtor RabbitMQ."""
        user = os.environ.get("RABBIT_USER", "guest")
        password = os.environ.get("RABBIT_PASSWORD", "guest")
        host = os.environ.get("RABBIT_HOST", "localhost")
        vhost = os.environ.get("RABBIT_VHOST", "/")
        port = os.environ.get("RABBIT_PORT", "5672")
        super().__init__(user=user, password=password, host=host, port=port, vhost=vhost)


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()