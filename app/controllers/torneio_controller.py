import json
from typing import Any, Dict, Tuple

from app.databases.mysql import MySQLConnection
from app.models.torneio_model import TorneioModel


class TorneioController:
    """Classe controller para Torneio."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def insert_torneio(self, request: Dict[str, Any]):
        """Função para isert de um novo time."""

        torneio_model = TorneioModel(self.database)
        torneio_model.create_table()

        torneio_model.nm_torneio_to = request.get("descricao_torneio", None)

        id_torneio = torneio_model.save()
        self.database.commit()
        return id_torneio
    
    def lista_de_torneios(self, id=0, nome=None):
        """Fução de consulta de torneios."""
        torneio_model = TorneioModel(self.database)
        todos = torneio_model.consulta_torneios(id, nome)
        return todos
