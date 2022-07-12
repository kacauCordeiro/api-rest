"""script criação para criação das tabelas do banco."""
import unittest

from app.controllers.eventos_controller import EventosController
from app.databases.mysql import MySQLConnection
from app.models.eventos_model import EnumEventos, EventosModel


class JogadorControllerTests(unittest.IsolatedAsyncioTestCase):
    """Classe de testes JogadorController."""
            
    async def test_evento_controller_inicio(self):
        """Teste de criação de um novo Jogador."""
        with MySQLConnection() as databases:
            eventos_model = EventosModel(databases)
            eventos_model.create_table()
            evento_controller = EventosController(databases)
            json = {
                    "detalhe_evento": "inicio_partida",
                    "id_jogador": "",
                    "metadados": {},
                    "data_hora": ""
                }
            result = evento_controller.evento_tempo(request=json, id_partida=1, tp_evento=EnumEventos.INICIO.value)
            print(result)
            self.assertEqual(type(result), int)