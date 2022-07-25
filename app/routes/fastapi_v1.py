import asyncio
from typing import Union
from fastapi import APIRouter, Query, Request, Depends, Cookie, HTTPException
from pyparsing import Optional
from fastapi.security import OAuth2PasswordBearer
from app.controllers.time_controller import TimeController
from app.controllers.jogador_controller import JogadorController
from app.controllers.transferencia_controller import TransferenciaController
from app.controllers.torneio_controller import TorneioController
from app.controllers.partidas_controller import PartidasController
from app.controllers.validacao_controller import ValidacaoController
from app.models.eventos_model import EnumEventos
from app.controllers.eventos_controller import EventosController
from app.databases.mysql import MySQLConnection

token_default = "Sorvete1234BatataFritaComM@ionese"

api_router_v1 = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        id = TimeController(database).insert_time(body)
        return {"id": id}

@api_router_v1.post("/jogador")
async def jogador(request: Request):
    """Enpoint para cadastrar jogador."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_jogador(request)
        body = await request.json()
        id = JogadorController(database).insert_jogador(body)
        return {"id": id} 
    
@api_router_v1.post("/transferencia")
async def transferencia(request: Request):
    """Enpoint para cadastrar transferencia."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_transferencia(request)
        body = await request.json()
        id = TransferenciaController(database).insert_transferencia(body)
        return {"id": id} 
    
@api_router_v1.post("/torneio")
async def torneio(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_torneio(request)
        body = await request.json()
        id = TorneioController(database).insert_torneio(body)
        return {"id": id} 
    
@api_router_v1.post("/partida")
async def partida(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_partida(request)
        body = await request.json()
        id = PartidasController(database).insert_partida(body)
        return {"id": id} 
# -------------------------------------------------------------------------------------------------------------------------------   
# GET
@api_router_v1.get("/times/")
async def get_times(id: int = 0, nome: str = None):
    """Enpoint para listar times com ou sem filtro."""
    with MySQLConnection() as database:
        return TimeController(database).lista_de_times(id=id, nome=nome)
    
@api_router_v1.get("/jogadores/")
async def get_jogadores(id: int = 0, nome: str = None):
    """"Enpoint para listar jogadores com ou sem filtro."""
    with MySQLConnection() as database:
        return JogadorController(database).lista_de_jogadores(id=id, nome=nome)
    
@api_router_v1.get("/torneios/")
async def get_torneios(id: int = 0, nome: str = None):
    """"Enpoint para listar torneios com ou sem filtro."""
    with MySQLConnection() as database:
        return TorneioController(database).lista_de_torneios(id=id, nome=nome)
    
@api_router_v1.get("/partidas/")
async def get_partidas(id_time: int = 0):
    """"Enpoint para listar partidas com ou sem filtro."""
    with MySQLConnection() as database:
        return PartidasController(database).lista_de_partidas(id_time)
    
@api_router_v1.get("/transferencias/")
async def get_transferencias(id_jogador: int = 0):
    """Enpoint para listar o historico de transferencias com ou sem filtro."""
    with MySQLConnection() as database:
        return TransferenciaController(database).historico_de_transferencias(id_jogador)

#EVENTOS
@api_router_v1.post("/partida/inicio/")
async def evento_inicio(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_evento(request=request, id_partida=id_partida, tp_evento=EnumEventos.INICIO.value)
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.INICIO.value)
        if eventos:
            return eventos

@api_router_v1.post("/partida/fim/")
async def evento_fim(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de fim da partida."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_evento(request=request, id_partida=id_partida, tp_evento=EnumEventos.FIM.value)
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.FIM.value)
        if eventos:
            return eventos

@api_router_v1.post("/partida/prorrogacao/")
async def evento_fim(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de prorrogacao da partida."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_evento(request=request, id_partida=id_partida, tp_evento=EnumEventos.PRORROGACAO.value)
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.PRORROGACAO.value)
        if eventos:
            return eventos

@api_router_v1.post("/partida/gol/")
async def evento_fim(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de gol da partida."""
    with MySQLConnection() as database:
        await ValidacaoController(database).valida_payload_evento(request=request, id_partida=id_partida, tp_evento=EnumEventos.GOL.value)
        body = await request.json()
        eventos = EventosController(database).evento_tempo(request=body, id_partida=id_partida, tp_evento=EnumEventos.GOL.value)
        if eventos:
            return eventos

@api_router_v1.delete("/partida/")
async def delete_partida(token: str = Depends(oauth2_scheme)):
    if token == token_default:
        return {"token": token}
