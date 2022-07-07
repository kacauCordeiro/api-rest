from typing import Any, Dict

from app.databases.mysql import MySQLConnection
from app.utils.rabbitmq import Rabbitmq

class EventosController:
    """Classe controller para eventos."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def evento_inicio(self, body, id_partida):
        """Função para insert de um evento de inicio."""
        Rabbitmq().publisher(queue_name='eventos', msg=body, exchange= "")
        return None