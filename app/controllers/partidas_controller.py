from typing import Any, Dict

from app.databases.mysql import MySQLConnection
from app.models.partidas_model import PartidasModel


class PartidasController:
    """Class controller player."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def insert_partida(self, request: Dict[str, Any]):
        """Função para isert de um novo player."""

        partida_model = PartidasModel(self.database)
        partida_model.create_table()

        partida_model.ds_partida_pt = request.get("descricao", None)
        partida_model.estadio_pt = request.get("estadio", "")
        partida_model.id_time_pt = request.get("id_time", "")
        partida_model.id_time_rival_pt = request.get("id_time_rival", "")
        partida_model.id_torneio_pt = request.get("id_torneio", "")

        id_partida = partida_model.save()
        self.database.commit()
        return id_partida

    def lista_de_partidas(self, id_time=0):
        """Function insert player."""
        partidas_model = PartidasModel(self.database)
        todos = partidas_model.consulta_partidas(id_time)
        return todos