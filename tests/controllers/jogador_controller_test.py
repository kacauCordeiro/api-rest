"""script criação para criação das tabelas do banco."""
import unittest

from app.controllers.jogador_controller import JogadorController
from app.databases.mysql import MySQLConnection


class JogadorControllerTests(unittest.IsolatedAsyncioTestCase):
    """Classe de testes JogadorController."""
            
    async def test_jogador_controller(self):
        """Teste de criação de um novo Jogador."""
        with MySQLConnection() as databases:
            jogador_controller = JogadorController(databases)
            json = {
                "nome_jogador": "Neymar", 
                "data_nascimento": "2000-12-28 00:00:00",
                "posicao": "atacante"
                }
            result = jogador_controller.insert_jogador(json)
            print(result)
            self.assertEqual(type(result), int)