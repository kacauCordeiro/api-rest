"""script criação para criação das tabelas do banco."""
import unittest

from app.controllers.time_controller import TimeController
from app.databases.mysql import MySQLConnection


class TimeControllerTests(unittest.IsolatedAsyncioTestCase):
    """Classe de testes TimeController."""

    async def test_time_controller(self):
        """Teste de criação de um novo Time."""
        with MySQLConnection() as databases:
            time_controller = TimeController(databases)
            json = {
                "nome_do_time": "Barcelona", 
                "classificacao": "B", 
                "localidade": "Barcelona"
                }
            result = time_controller.insert_time(json)
            print(result)
            self.assertEqual(type(result), int)
