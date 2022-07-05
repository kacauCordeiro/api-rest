from typing import Union

from .model import Model


class JogadorModel(Model):
    """Classe modelo para jogador."""

    _table = "JOGADOR"
    _suffix = "jg"
    _pk = "id_jogador_jg"

    nm_jogador_jg: Union[str, None] = None
    dt_nascimento_jg: Union[str, None] = None
    ps_jogador_jg: Union[str, None] = None
    #id_time_jg = Union[int, None] = None

    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS JOGADOR (
                    ID_JOGADOR_JG INT(8) NOT NULL AUTO_INCREMENT,
                    NM_JOGADOR_JG VARCHAR(100) NOT NULL UNIQUE,
                    DT_NASCIMENTO_JG datetime NOT NULL,
                    PS_JOGADOR_JG VARCHAR(12),
                    ID_TIME_JG INT(8) NOT NULL,
                PRIMARY KEY (ID_JOGADOR_JG),
                FOREIGN KEY (ID_TIME_JG) REFERENCES TIME(ID_TIME_TM)
                );"""
        self.query_raw(query)
        
    def list_jogadores(self, args=None):
        """Lista todos os jogadores de acordo com o filtro."""
        include_where = ''
        if args:
            if args == "name":
                include_where = f" WHERE NM_JOGADOR_JG LIKE '%{args}%'"
            if args == "id":
                include_where = f" WHERE ID_JOGADOR_JG = {args}"
        query = f""" SELECT * FROM JOGADOR {include_where}"""
        
        result = self.query_raw(query)
        
        return result.fetchall()
        
