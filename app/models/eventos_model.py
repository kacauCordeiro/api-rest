import json
from enum import Enum
from typing import Union, Dict
from datetime import datetime
from .model import Model

class EnumEventos(Enum):
    """Enum para status de eventos."""
    INICIO = "INICIO"
    FIM = "FIM"
    PRORROGACAO = "PRORROGACAO"
    GOL = "GOL"
    FALTA = "FALTA"
    CARTAO = "CARTAO"

class EventosModel(Model):
    """Classe modelo para eventos."""

    _table = "EVENTOS"
    _suffix = "EV"
    _pk = "id_evento_ev"

    id_evento_ev: Union[int, None] = None
    id_partida_ev: Union[int, None] = None
    tp_evento_ev: Union[str, None] = None
    ds_evento_ev: Union[str, None] = None
    id_jogador_ev: Union[int, None] = None
    json_evento_ev: Union[Dict, None] = None
    dt_evento_ev: Union[str, None, datetime] = None
    qt_gol_time_ev: Union[int, None] = None
    qt_gol_rival_ev: Union[int, None] = None

    def create_table(self):
        """Cria uma tabela para eventos se não existir."""
        query = """ CREATE TABLE IF NOT EXISTS EVENTOS (
                    ID_EVENTO_EV INT(8) NOT NULL AUTO_INCREMENT,
                    ID_PARTIDA_EV INT(8) NOT NULL,
                    ID_TIME_EV INT(8),
                    ID_JOGADOR_EV  INT(8),
                    TP_EVENTO_EV VARCHAR(50) NOT NULL,
                    JSON_EVENTO_EV JSON,
                    DS_EVENTO_EV VARCHAR(200),
                    DT_EVENTO_EV datetime,
                    QT_GOL_TIME_EV INT(8),
                    QT_GOL_RIVAL_EV INT(8),
                PRIMARY KEY (ID_EVENTO_EV),
                FOREIGN KEY (ID_PARTIDA_EV) REFERENCES PARTIDAS(ID_PARTIDA_PT),
                FOREIGN KEY (ID_JOGADOR_EV) REFERENCES JOGADOR(ID_JOGADOR_JG),
                FOREIGN KEY (ID_TIME_EV) REFERENCES TIME(ID_TIME_TM)
                ); """
        self.query_raw(query)

    
    def consulta_eventos_partida(self, id_partida=0):
        """Lista todas os eventos de acordo com o filtro."""
        include_where = ''
        if id_partida:
            include_where = f" WHERE ID_PARTIDA_EV = {id_partida}"

        query = f""" SELECT * FROM EVENTOS {include_where}  ORDER BY ID_EVENTO_EV DESC"""
        
        result = self.query_raw(query)
        
        return result.fetchall()