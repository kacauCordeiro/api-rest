import asyncio
from typing import Union
from fastapi import APIRouter, Query, Request, Depends, Cookie, HTTPException
from pyparsing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.controllers.time_controller import TimeController
from app.controllers.jogador_controller import JogadorController
from app.controllers.transferencia_controller import TransferenciaController
from app.controllers.torneio_controller import TorneioController
from app.controllers.partidas_controller import PartidasController
from app.controllers.validacao_controller import ValidacaoController
from app.models.eventos_model import EnumEventos
from app.controllers.eventos_controller import EventosController
from app.databases.mysql import MySQLConnection

api_router_v1 = APIRouter()

@api_router_v1.get("/healthcheck")
async def healthcheck():
    return {"message": "A API está ativa!"}
# POST
@api_router_v1.post("/time")
async def time(request: Request):
    """Enpoint para cadastrar time."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_time(request)
        body = await request.json()
        return TimeController(database).insert_time(body)

@api_router_v1.post("/jogador")
async def jogador(request: Request):
    """Enpoint para cadastrar jogador."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_jogador(request)
        body = await request.json()
        return JogadorController(database).insert_jogador(body)
    
@api_router_v1.post("/transferencia")
async def transferencia(request: Request):
    """Enpoint para cadastrar transferencia."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_transferencia(request)
        body = await request.json()
        return TransferenciaController(database).insert_transferencia(body)
    
@api_router_v1.post("/torneio")
async def torneio(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_torneio(request)
        body = await request.json()
        return TorneioController(database).insert_torneio(body)
    
@api_router_v1.post("/partida")
async def partida(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_partida(request)
        body = await request.json()
        return PartidasController(database).insert_partida(body)
# -------------------------------------------------------------------------------------------------------------------------------   
# GET
@api_router_v1.get("/times/")
async def get_times(id: int = 0, nome: str = None):
    """Enpoint para listar todos os times com e sem filtro."""
    with MySQLConnection() as database:
        return TimeController(database).lista_de_times(id=id, nome=nome)
    
@api_router_v1.get("/jogadores/")
async def get_jogadores(id: int = 0, nome: str = None):
    """"Enpoint para listar todos os jogadores com e sem filtro."""
    with MySQLConnection() as database:
        return JogadorController(database).lista_de_jogadores(id=id, nome=nome)
    
@api_router_v1.get("/torneios/")
async def get_torneios(name: str = None):
    """"Enpoint para listar todos os torneios com e sem filtro."""
    with MySQLConnection() as database:
        return TorneioController(database).lista_de_torneios(name)
    
@api_router_v1.get("/partidas/")
async def get_partidas(id_time: int = 0):
    """"Enpoint para listar todas as partidas com e sem filtro."""
    with MySQLConnection() as database:
        return PartidasController(database).lista_de_partidas(id_time)
    
@api_router_v1.get("/transferencias/")
async def get_transferencias(id_jogador: int = 0):
    """Enpoint para listar o historico de transferencias com e sem filtro."""
    with MySQLConnection() as database:
        return TransferenciaController(database).historico_de_transferencias(id_jogador)

#EVENTOS
@api_router_v1.post("/partida/inicio/")
async def evento_inicio(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_partida(request=request, id_partida=id_partida, tp_evento=EnumEventos.INICIO.value)
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.INICIO.value)
        if eventos:
            return eventos

@api_router_v1.post("/partida/fim/")
async def evento_fim(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.FIM.value)
        if eventos:
            return eventos

@api_router_v1.post("/partida/prorrogacao/")
async def evento_fim(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.PRORROGACAO.value)
        if eventos:
            return eventos
