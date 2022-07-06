from typing import Any, Dict

from app.databases.mysql import MySQLConnection
from app.models.jogador_model import JogadorModel


class EventosController:
    """Class controller player."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def evento_inicio(self, id):
        """Função para isert de um novo player."""
        return None