import datetime
import json
from typing import Any, Dict
from app.utils.logger import Logger
from app.databases.mysql import MySQLConnection
from app.models.eventos_model import EventosModel, EnumEventos
from app.utils.rabbitmq import Rabbitmq

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger = Logger() 

class EventosController:
    """Classe controller para eventos."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database
    
    def publisher_evento(self, evento):
        rq = Rabbitmq()
        rq.publisher(queue_name='eventos', msg=json.dumps(evento), exchange="eventos", routing_key="eventos")

    def evento_tempo(self, request: Dict[str, Any], id_partida=0, tp_evento=""):
        """Função para insert de um evento que marca o tempo."""
        if id_partida:
            eventos_model = EventosModel(self.database)
            eventos_model.id_partida_ev = id_partida
            eventos_model.tp_evento_ev = tp_evento
            eventos_model.ds_evento_ev = request.get("detalhe_evento", "")
            eventos_model.json_evento_ev = request.get("metadados", {})
            eventos_model.qt_gol_time_ev = request.get("gols_time", 0)
            eventos_model.qt_gol_rival_ev = request.get("gols_rival", 0)
            eventos_model.dt_evento_ev = now
            evento = eventos_model.save()
            self.database.commit()
            
            request["id_evento"] = evento
            request["id_partida"] = id_partida
            request["tp_evento"] = tp_evento
            request["placar"] = f'{eventos_model.qt_gol_time_ev}x{eventos_model.qt_gol_rival_ev}'
            
            self.publisher_evento(request)
            
            return request
        
    def evento_fim(self, request: Dict[str, Any], id_partida=0):
        """Função para insert de um evento de inicio."""
        if id_partida:
            eventos_model = EventosModel(self.database)
            eventos_model.id_partida_ev = request.get("id_partida", 0)
            eventos_model.tp_evento_ev = EnumEventos.INICIO
            eventos_model.ds_evento_ev = request.get("detalhe_evento", "")
            eventos_model.id_jogador_ev = request.get("id_jogador", 0)
            eventos_model.json_evento_ev = request.get("metadados", {})
            if not request.get('data_hora'):
                eventos_model.dt_evento_ev = request.get("metadados", str(now))
            eventos_model.save()
            
            rq = Rabbitmq()
            request["id_partida"] = id_partida
            rq.publisher(queue_name='eventos', msg=request, exchange="eventos", routing_key="eventos")

            return eventos_model