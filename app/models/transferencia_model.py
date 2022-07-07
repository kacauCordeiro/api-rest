from typing import Union
from datetime import datetime
from .model import Model


class TransferenciatoModel(Model):
    """Classe modelo para transferencia."""

    _table = "TRANSFERENCIA"
    _suffix = "ct"
    _pk = "id_transfer_tfr"

    id_jogador_tfr: Union[int, None] = None
    id_time_origem_tfr: Union[int, None] = None
    id_time_destino_tfr: Union[int, None] = None
    vl_transfer_tfr: Union[str, None] = None
    dt_transfer_tfr: Union[str, None, datetime] = None

    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS TRANSFERENCIA (
                    ID_TRANSFER_TFR INT(8) NOT NULL AUTO_INCREMENT,
                    ID_JOGADOR_TFR INT(8) NOT NULL,
                    ID_TIME_ORIGEM_TFR  INT(8) NOT NULL,
                    ID_TIME_DESTINO_TFR INT(8) NOT NULL,
                    VL_TRANSFER_TFR VARCHAR(15) NOT NULL,
                    DT_TRANSFER_TFR datetime,
                PRIMARY KEY (ID_TRANSFER_TFR),
                FOREIGN KEY (ID_TIME_ORIGEM_TFR) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TIME_DESTINO_TFR) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_JOGADOR_TFR) REFERENCES JOGADOR(ID_JOGADOR_JG)
                );"""
        self.query_raw(query)

    
    def consulta_transferencias(self, id_jogador=0):
        """Lista todas as transferencias de acordo com o filtro."""
        include_where = ''
        if id_jogador:
            include_where = f" WHERE ID_JOGADOR_TFR = {id_jogador}"

        query = f""" SELECT * FROM TRANSFERENCIA {include_where}  ORDER BY ID_TRANSFER_TFR DESC"""
        
        result = self.query_raw(query)
        
        return result.fetchall()