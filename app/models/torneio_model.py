from typing import Union

from .model import Model


class TorneioModel(Model):
    """Classe modelo para torneio."""

    _table = "TORNEIO"
    _suffix = "to"
    _pk = "id_torneio_to"

    nm_torneio_to: Union[str, None] = None

    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS TORNEIO (
                    ID_TORNEIO_TO INT(8) NOT NULL AUTO_INCREMENT,
                    NM_TORNEIO_TO VARCHAR(100) NOT NULL UNIQUE,
                PRIMARY KEY (ID_TORNEIO_TO)
                );"""
        self.query_raw(query)

    
    def consulta_torneios(self, id=0, nome=None):
        """Lista todos os torneios de acordo com o filtro."""
        include_where = ''
        if nome:
            include_where = f" WHERE NM_TORNEIO_TO LIKE '%{nome}%'"
        if id:
            include_where = f" WHERE ID_TORNEIO_TO = {id}"

        query = f""" SELECT * FROM TORNEIO {include_where}"""
        
        result = self.query_raw(query)
        
        return result.fetchall()