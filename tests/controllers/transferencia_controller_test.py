"""script criação para criação das tabelas do banco."""
import datetime
import unittest

from app.controllers.transferencia_controller import TransferenciaController
from app.databases.mysql import MySQLConnection


class TransferenciaControllerTests(unittest.IsolatedAsyncioTestCase):
    """Classe de testes TransferenciaController."""
            
    async def test_transferencia_controller(self):
        """Testa função controller insert transferencia."""
        with MySQLConnection() as databases:
            transferencia_controller =  TransferenciaController(databases)
            json = {
                "id_jogador": 1, 
                "id_time_origem": 1,
                "id_time_destino": 8,
                "data": "2022-02-01 00:00:00",
                "vl_transferencia": "50.000"
                }
            result = transferencia_controller.insert_transferencia(json)
            print(result)
            self.assertEqual(type(result), int)