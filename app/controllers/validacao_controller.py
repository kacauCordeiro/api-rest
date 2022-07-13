import json
import os
from datetime import datetime
from typing import Any, Dict, Set, Tuple
from app.models.eventos_model import EnumEventos
from app.models.jogador_model import JogadorModel
from app.models.partidas_model import PartidasModel
from app.models.time_model import TimeModel

from fastapi import HTTPException, Request
from app.databases.mysql import MySQLConnection
from app.models.torneio_model import TorneioModel
from app.utils.logger import Logger

class ValidacaoController:
    """Classe controller para validacao."""
    
    
    def __init__(self, database: MySQLConnection) -> None:
        """Inicialização da classe.

        Args:
            database (MySQLConnection): instancia do banco de dados.
        """
        self.database = database
        
    time_fields = (
        "nome_do_time",
        "classificacao",
        "localidade",
    )
    
    jogador_fields = (
        "nome_jogador",
        "data_nascimento",
        "posicao",
        "id_time",
    )
    
    transferencia_fields = (
        "id_jogador",
        "id_time_origem",
        "id_time_destino",
        "vl_transferencia",
        "data",
    )
    
    torneio_fields = (
        "descricao_torneio",
    )
    
    partida_fields = (
        "id_time",
        "id_time_rival",
        "id_torneio",
        "descricao",
        "estadio",
    )
    
    evento_fim_fields = (
        "qt_gol_time_ev",
        "qt_gol_rival_ev",
    )

    async def valida_payload_time(self, request: Request):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        required_fields = ValidacaoController.time_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model = TimeModel(self.database)
        time_model.ds_time_tm = body.get("nome_do_time")
        time = time_model.consulta_times(nome=body.get("nome_do_time"))
        
        if time:
            errors.update({"duplicidade": "O time já está cadastrado, não é possível criar times com o mesmo nome"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
    
    async def valida_payload_jogador(self, request: Request):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        required_fields = ValidacaoController.jogador_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        jogador_model = JogadorModel(self.database)
        jogador_model.nm_jogador_jg = body.get("nome_jogador")
        jogador = jogador_model.consulta_jogadores(nome=body.get("nome_jogador"))
        
        if jogador:
            errors.update({"duplicidade": "O jogador já está cadastrado, não é possível cadastrar um jogador com o mesmo nome"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model = TimeModel(self.database)
        time_model.ds_time_tm = body.get("id_time")
        time = time_model.consulta_times(id=body.get("id_time"))
        
        if not time:
            errors.update({"invalido": "O time informado não existe"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
    
    async def valida_payload_transferencia(self, request: Request):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        required_fields = ValidacaoController.transferencia_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        jogador_model = JogadorModel(self.database)
        jogador_model.nm_jogador_jg = body.get("id_jogador")
        jogador = jogador_model.consulta_jogadores(nome=body.get("id_jogador"))
        
        if jogador:
            errors.update({"invalido": "O jogador informado não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model_origem = TimeModel(self.database)
        time_model_origem.ds_time_tm = body.get("id_time_origem")
        time_origem = time_model_origem.consulta_times(id=body.get("id_time_origem"))
        Logger().info(jogador)
        if not time_origem or jogador_model.id_time_jg != time_origem:
            errors.update({"invalido": "O time origem informado não existe ou é diferente do time atual do jogador."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model_destino = TimeModel(self.database)
        time_model_destino.ds_time_tm = body.get("id_time_origem")
        time_destino = time_model_destino.consulta_times(id=body.get("id_time_origem"))
        
        if not time_destino or time_origem==time_destino:
            errors.update({"invalido": "O time destino informado não existe ou é igual ao time origem"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
    async def valida_payload_torneio(self, request: Request):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        required_fields = ValidacaoController.torneio_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        torneio_model = TorneioModel(self.database)
        torneio_model.nm_torneio_to = body.get("descricao_torneio")
        torneio = torneio_model.consulta_torneios(nome=body.get("descricao_torneio"))
        
        if torneio:
            errors.update({"duplicidade": "O torneio já está cadastrado, não é possível cadastrar um torneio com o mesmo nome."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
    async def valida_payload_partida(self, request: Request):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        required_fields = ValidacaoController.partida_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model = TimeModel(self.database)
        time_model.id_time_tm = body.get("id_time")
        time = time_model.consulta_times(id=body.get("id_time"))

        if not time:
            errors.update({"invalido": "O id_time informado não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        rival_model = TimeModel(self.database)
        rival_model.id_time_tm = body.get("id_time_rival")
        rival = rival_model.consulta_times(id=body.get("id_time_rival"))
        
        if not rival or time==rival:
            errors.update({"invalido": "O id_time_rival informado não existe ou é igual ao id_time"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        torneio_model = TorneioModel(self.database)
        torneio_model.id_torneio_to = body.get("id_torneio")
        torneio = torneio_model.consulta_torneios(id=body.get("id_torneio"))
        
        if not torneio:
            errors.update({"invalido": "O torneio informado não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
    async def valida_payload_evento(self, request: Request, id_partida=0, tp_evento=None):
        """Valida o payload.

        Args:
            request (Request): requisição assíncrona do fastapi
        """
        body = await request.json()
        errors: Dict[str, str] = {}
        is_valid_body = True

        credentials = body.get("credentials")
        
        if not id_partida:
            errors.update({"invalido": "A partida não foi informada."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        partida_model = PartidasModel(self.database)
        partida_model.id_partida_pt = id_partida
        partida = partida_model.consulta_partidas(id_partida=id_partida)
        
        if not partida:
            errors.update({"invalido": "A partida informada não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        if not tp_evento:
            errors.update({"invalido": "O evento não foi informado."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        if tp_evento == EnumEventos.INICIO:
            return True
        
        if tp_evento == EnumEventos.FIM:
            required_fields = ValidacaoController.evento_fim_fields

        is_valid_body, fields = ValidacaoController.check_required_fields(
            fields=required_fields,
            payload=body,
        )
        
        if not is_valid_body:
            errors = {field: f"O campo {field} é vazio ou não foi enviado" for field in fields}
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        time_model = TimeModel(self.database)
        time_model.id_time_tm = body.get("id_time")
        time = time_model.consulta_times(id=body.get("id_time"))

        if not time:
            errors.update({"invalido": "O id_time informado não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        rival_model = TimeModel(self.database)
        rival_model.id_time_tm = body.get("id_time_rival")
        rival = rival_model.consulta_times(id=body.get("id_time_rival"))
        
        if not rival or time==rival:
            errors.update({"invalido": "O id_time_rival informado não existe ou é igual ao id_time"})
            raise self.__has_errors(body, errors, insert_failed_request=False)
        
        torneio_model = TorneioModel(self.database)
        torneio_model.id_torneio_to = body.get("id_torneio")
        torneio = torneio_model.consulta_torneios(id=body.get("id_torneio"))
        
        if not torneio:
            errors.update({"invalido": "O torneio informado não existe."})
            raise self.__has_errors(body, errors, insert_failed_request=False)
    
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
    
    def __has_errors(self, body: dict, errors: dict, insert_failed_request: bool = True):
        """Tratamento de errors.

        Args:
            body (dict): corpo da requisição
            errors (dict): Uma dict contendo os erros \
                encontrados durante o processo de validação.
            insert_failed_request (bool): Flag para ver se será necessário \
                inserir registro no banco.

        Returns:
            erros, 400: Response
        """
        if insert_failed_request:
            self.__add_failed_request(body)
        return HTTPException(detail=errors, status_code=400)