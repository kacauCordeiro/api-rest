from typing import Union

from .model import Model


class PartidasModel(Model):
    """Classe modelo para partidas."""

    _table = "PARTIDAS"
    _suffix = "pt"
    _pk = "id_partida_pt"

    ds_partida_pt: Union[str, None] = None
    estadio_pt: Union[str, None]
    
    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS PARTIDAS (
                    ID_PARTIDA_PT INT(8) NOT NULL AUTO_INCREMENT,
                    DS_PARTIDA_PT VARCHAR(255) NOT NULL,
                    ESTADIO_PT VARCHAR(255) NOT NULL,
                    ID_TIME_PT INT(8) NOT NULL,
                    ID_TIME_RIVAL_PT INT(8) NOT NULL,
                    ID_TORNEIO_PT INT(8) NOT NULL,
                PRIMARY KEY (ID_PARTIDA_PT),
                FOREIGN KEY (ID_TIME_PT) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TIME_RIVAL_PT) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TORNEIO_PT) REFERENCES TORNEIO(ID_TORNEIO_TO)
                );"""
        self.query_raw(query)

    
    def consulta_partidas(self,id_partida=0, id_time=0):
        """Lista todos os jogadores de acordo com o filtro."""
        include_where = ''
        if id_partida:
            include_where = f" WHERE ID_PARTIDA_PT = {id_partida} "
        if id_time:
            include_where = f" WHERE ID_TIME_PT = {id_time} OR ID_TIME_RIVAL_PT = {id_time}"

        query = f""" SELECT * FROM PARTIDAS {include_where}"""
        
        result = self.query_raw(query)
        
        return result.fetchall()