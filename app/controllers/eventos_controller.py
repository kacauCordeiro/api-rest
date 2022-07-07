from typing import Any, Dict

from app.databases.mysql import MySQLConnection

class EventosController:
    """Classe controller para eventos."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def evento_inicio(self, id):
        """Função para insert de um evento de inicio."""
        return None