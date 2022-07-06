import json
from typing import Any, Dict, Tuple

from app.databases.mysql import MySQLConnection
from app.models.time_model import TimeModel


class TimeController:
    """Classe controller para time."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def insert_time(self, request: Dict[str, Any]):
        """Função para isert de um novo time."""

        time_model = TimeModel(self.database)
        time_model.create_table()

        time_model.ds_time_tm = request.get("nome_do_time", None)
        time_model.classificacao_time_tm = request.get("classificacao", "")
        time_model.ds_localidade_tm = request.get("localidade", "")

        id_time = time_model.save()
        self.database.commit()
        return id_time

