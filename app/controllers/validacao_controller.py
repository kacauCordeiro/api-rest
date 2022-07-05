from typing import Any, Dict, Tuple, Set

from app.databases.mysql import MySQLConnection

class ValidacaoController:
    """Classe controller para validacao."""
    
    
    def __init__(self, database: MySQLConnection) -> None:
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database
        
    template_jogador_fields = (
        "nome_jogador",
        "data_nascimento",
        "id_time",
    )

    template_time_fields = (
       "nome_do_time", 
       "classificacao",
       "localidade",
    )

    template_transferencia_fields = (
        "cardWidth",
        "contents",
    )
    
    @staticmethod
    def check_required_fields(fields: tuple, payload) -> Tuple[bool, Set[Any]]:
        """Verifica se os campos requeridos estão no dicionário informado.

        Args:
            fields (tuple): lista com os nomes dos campos requerido
            payload (dict): dicionário onde iremos verificar se os campos foram enviados

        Returns:
            bool, list: [description]
        """
        result = list(filter(lambda x: payload.get(x, False), fields))
        return (len(result) == len(fields)), (set(fields) - set(result))