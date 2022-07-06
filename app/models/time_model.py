from typing import Union

from .model import Model


class TimeModel(Model):
    """Classe modelo para time."""

    _table = "TIME"
    _suffix = "tm"
    _pk = "id_time_tm"

    ds_time_tm: Union[str, None] = None
    ds_localidade_tm: Union[str, None]
    classificacao_time_tm: Union[str, None] = None

    def create_table(self):
        """Create table if not exists function."""
        query = """ CREATE TABLE IF NOT EXISTS TIME (
                    ID_TIME_TM INT(8) NOT NULL AUTO_INCREMENT,
                    DS_TIME_TM VARCHAR(100) NOT NULL UNIQUE,
                    DS_LOCALIDADE_TM VARCHAR(100) NOT NULL,
                    CLASSIFICACAO_TIME_TM VARCHAR(4) NOT NULL,
                PRIMARY KEY(ID_TIME_TM)
                );"""
        self.query_raw(query)
