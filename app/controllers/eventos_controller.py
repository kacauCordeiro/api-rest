import datetime
from typing import Any, Dict
from app.databases.mysql import MySQLConnection
from app.models.eventos_model import EventosModel,EnumEventos
from app.utils.rabbitmq import Rabbitmq

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

class EventosController:
    """Classe controller para eventos."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def evento_inicio(self, request: Dict[str, Any], id_partida=0):
        """Função para insert de um evento de inicio."""
        if id_partida:
            eventos_model = EventosModel(self.database)
            eventos_model.id_partida_ev = request.get("id_partida", 0)
            eventos_model.tp_evento_ev = EnumEventos.INICIO
            eventos_model.ds_evento_ev = request.get("detalhe_evento", "")
            eventos_model.id_jogador_evento = request.get("id_jogador", 0)
            eventos_model.json_evento_ev = request.get("metadados", {})
            if not request.get('data_hora'):
                eventos_model.dt_evento_ev = request.get("metadados", str(now))
            eventos_model.save()
            
            rq = Rabbitmq()
            request["id_partida"] = id_partida
            rq.publisher(queue_name='eventos', msg=request, exchange="eventos", routing_key="eventos")

            return eventos_model