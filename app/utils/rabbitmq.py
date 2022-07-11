import pika
import json
import os

class Rabbitmq:
    
    def __init__(self):
        """Construtor RabbitMQ."""
        user = os.environ.get("RABBIT_USER", "guest")
        password = os.environ.get("RABBIT_PASSWORD", "guest")
        host = os.environ.get("RABBIT_HOST", "rabbitmq.apirest_default")
        vhost = os.environ.get("RABBIT_VHOST", "/")
        port = os.environ.get("RABBIT_PORT", '5672')

        self.connection = None      
        try:
            credentials = pika.PlainCredentials('guest', 'guest')
            self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq.apirest_default',5672,'/',credentials))
            
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="eventos")
            self.channel.exchange_declare(exchange="eventos", exchange_type='fanout')
            self.channel.queue_bind(exchange="eventos", queue="eventos")
        except Exception as err:  # pylint: disable=broad-except
            print("[RABBIT_CONNECTION_ERROR] Não foi possivel conectar!", err)

    def close(self):
        """Fecha conexão com o rabbit."""
        if self.connection.is_open:
            self.channel.close()
            self.connection.close()
    
    def publisher(self, queue_name: str, msg: dict, exchange: str = "", priority: int = 1, routing_key: str = ""):
        "Publica uma mensagem na fila."
        
        try:
            result = {"msg": "não funcionou"}
            if self.connection:
                self.channel.basic_publish(exchange=exchange,routing_key=routing_key,body=json.dumps(msg))
        except Exception as err:
            print("[RABBIT_PUBLISH_ERROR] Não foi possível enviar mensagem!", err)
        return self.connection
