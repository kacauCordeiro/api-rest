from typing import Union

from .model import Model


class TorneioModel(Model):
    """Classe modelo para torneio."""

    _table = "TORNEIO"
    _suffix = "to"
    _pk = "id_torneio_to"

    ds_torneio_to: Union[str, None] = None

    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS TORNEIO (
                    ID_TORNEIO_TO INT(8) NOT NULL AUTO_INCREMENT,
                    NM_TORNEIO_TO
                PRIMARY KEY(ID_TORNEIO_TO)
                );"""
        self.query_raw(query)
