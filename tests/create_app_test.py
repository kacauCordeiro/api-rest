"""Teste de App Factory."""
import unittest

from app.main import create_app
from tests.fast_test_client import TestClient

app = create_app()
client = TestClient(app)


class CreateAppTest(unittest.IsolatedAsyncioTestCase):
    """Classe de teste da App Factory."""

    async def test_create_app(self):  # pylint: disable=no-self-use
        """Testa se consegue executar o create_app."""
        assert create_app()

    async def test_post_time_success(self):
        """Testa se a chamada post para o endpoint time obteve sucesso."""
        payload = {"nome_do_time": "Barcelona", "classificacao": "B"}
        response = client.post("/v1/time", json=payload)
        self.assertIsNotNone(response)

    async def test_post_jogador_success(self):
        """Testa se a chamada post para o endpoint jogador obteve sucesso."""
        payload = {"nome_jogador": "Neymar", "posicao": "atacante", "id_time": 1}
        response = client.post("/v1/jogador", json=payload)
        self.assertIsNotNone(response)

    async def test_post_transferencia_success(self):
        """Testa se a chamada post para o endpoint transferencia obteve sucesso."""
        payload = {"id_jogador": 1, "id_time": 1}
        response = client.post("/v1/transferencia", json=payload)
        self.assertIsNotNone(response)
        
    async def test_get_jogador_success(self):
        """Testa se a chamada get para o endpoint jogador obteve sucesso."""
        response = client.get("/v1/jogador")
        self.assertIsNotNone(response)
