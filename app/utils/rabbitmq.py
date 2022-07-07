import pika
import json
import os

class Rabbitmq:
    
    def __init__(self):
        """Construtor RabbitMQ."""
        self.__config = {
            "heartbeat": 600,
            "host": os.environ.get("RABBIT_HOST", "localhost"),
            "port": os.environ.get("RABBIT_PORT", "5672"),
            "credentials": pika.PlainCredentials(
                os.environ.get("RABBIT_USER", "guest"), os.environ.get("RABBIT_PASSWORD", "guest")
            )
        }

        self.connection = None      
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.__config))
            self.channel = self.connection.channel()

        except Exception as err:  # pylint: disable=broad-except
            print("[RABBIT_CONNECTION_ERROR] Não foi possivel conectar!", err)

    def close(self):
        """Fecha conexão com o rabbit."""
        if self.connection.is_open:
            self.channel.close()
            self.connection.close()
    
    def publisher(self, queue_name: str, msg: dict, exchange: str = "", priority: int = 1):
        "Publica uma mensagem na fila."
        try:
            if self.connection:
                self.channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
                self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=queue_name,
                    body=json.dumps(msg),
                    properties=pika.BasicProperties(delivery_mode=2, priority=priority),
                )
                result = True

        except Exception as err:
            print("[RABBIT_PUBLISH_ERROR] Não foi possível enviar mensagem!", err)
            result = False
        return result
