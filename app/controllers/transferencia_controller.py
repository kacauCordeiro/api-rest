import datetime
from typing import Any, Dict

from app.databases.mysql import MySQLConnection
from app.models.transferencia_model import TransferenciatoModel
from app.models.jogador_model import JogadorModel


class TransferenciaController:
    """Classe controller para Transferencia."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def insert_transferencia(self, request: Dict[str, Any]):
        """Função para isert de uma nova transferencia."""

        transferencia_model = TransferenciatoModel(self.database)
        transferencia_model.create_table()

        transferencia_model.id_jogador_tfr = int(request.get("id_jogador", 0))
        transferencia_model.id_time_origem_tfr = int(request.get("id_time_origem", 0))
        transferencia_model.id_time_destino_tfr = int(request.get("id_time_destino", 0))
        transferencia_model.vl_transfer_tfr = request.get("vl_transferencia", "")
        transferencia_model.dt_transfer_tfr = request.get("data", str(datetime.datetime.now()))

        id_transferencia = transferencia_model.save()
        
        if id_transferencia:
            jogador_model = JogadorModel(self.database)
            jogador_model.id_jogador_jg = int(request.get("id_jogador", 0))
            jogador_model.id_time_jg = int(request.get("id_time_destino", 0))
        
        self.database.commit()

        return id_transferencia
