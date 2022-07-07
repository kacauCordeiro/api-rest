from typing import Any, Dict

from app.databases.mysql import MySQLConnection
from app.models.jogador_model import JogadorModel


class JogadorController:
    """Classe controller para jogadores."""

    def __init__(self, database: MySQLConnection):
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database

    def insert_jogador(self, request: Dict[str, Any]):
        """Função de inserção para um novo jogador."""

        jogador_model = JogadorModel(self.database)
        jogador_model.create_table()
        
        if not request.get("nome_jogador"):
            return 

        jogador_model.nm_jogador_jg = request.get("nome_jogador", None)
        jogador_model.dt_nascimento_jg = request.get("data_nascimento", "")
        jogador_model.ps_jogador_jg = request.get("posicao", "")
        jogador_model.id_time_jg = request.get("id_time", "")

        id_jogador = jogador_model.save()
        self.database.commit()
        return id_jogador
    
    def lista_de_jogadores(self, id=0, nome=None):
        """Function insert player."""
        jogador_model = JogadorModel(self.database)
        todos = jogador_model.consulta_jogadores(id, nome)
        return todos
