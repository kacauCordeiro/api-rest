import asyncio
from typing import Union
from fastapi import APIRouter, Query, Request, Depends, Cookie
from pyparsing import Optional

from app.controllers.time_controller import TimeController
from app.controllers.jogador_controller import JogadorController
from app.controllers.transferencia_controller import TransferenciaController
from app.controllers.torneio_controller import TorneioController
from app.controllers.partidas_controller import PartidasController
from app.controllers.eventos_controller import EventosController
from app.databases.mysql import MySQLConnection

api_router_v1 = APIRouter()


class DependencyClass:
    async def async_dep(self, request: Request):
        await asyncio.sleep(0)
        return False

    def sync_dep(self, request: Request):
        return True
dependency = DependencyClass()

@api_router_v1.get("/healthcheck")
async def healthcheck():
    return {"message": "A API está ativa!"}
# POST
@api_router_v1.post("/time")
async def time(request: Request):
    """Enpoint para cadastrar time."""
    with MySQLConnection() as database:
        body = await request.json()
        return TimeController(database).insert_time(body)

@api_router_v1.post("/jogador")
async def jogador(request: Request):
    """Enpoint para cadastrar jogador."""
    with MySQLConnection() as database:
        body = await request.json()
        return JogadorController(database).insert_jogador(body)
    
@api_router_v1.post("/transferencia")
async def transferencia(request: Request):
    """Enpoint para cadastrar transferencia."""
    with MySQLConnection() as database:
        body = await request.json()
        return TransferenciaController(database).insert_transferencia(body)
    
@api_router_v1.post("/torneio")
async def torneio(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        body = await request.json()
        return TorneioController(database).insert_torneio(body)
    
@api_router_v1.post("/partida")
async def partida(request: Request):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
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


# DELETE
@api_router_v1.delete("/time/{id}")
async def time(id: int = 0):
    """Enpoint para cadastrar time."""
    with MySQLConnection() as database:
        return TimeController(database).delete()

@api_router_v1.delete("/jogador/{id}")
async def jogador(id: int = 0):
    """Enpoint para cadastrar jogador."""
    with MySQLConnection() as database:
        return JogadorController(database).delete_jogador(id)
    
@api_router_v1.delete("/transferencia/{id}")
async def transferencia(id: int = 0):
    """Enpoint para cadastrar transferencia."""
    with MySQLConnection() as database:
        return TransferenciaController(database).delete_transferencia(id)
    
@api_router_v1.delete("/torneio/{id}")
async def torneio(id: int = 0):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        return TorneioController(database).delete_torneio(id)
    
@api_router_v1.delete("/partida/{id}")
async def partida(id: int = 0):
    """Enpoint para cadastrar torneio."""
    with MySQLConnection() as database:
        return PartidasController(database).delete_partida(id)



#UPDATE

#EVENTOS
@api_router_v1.post("/partida/inicio/")
async def evento_inicio(request: Request, id_partida: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        body = await request.json()
        eventos = EventosController(database).evento_inicio(body, id_partida)
        if eventos:
            return body



# def query_extractor(q: Union[str, None] = None):
#     return q


# def query_or_cookie_extractor(
#     q: str = Depends(query_extractor),
#     last_query: Union[str, None] = Cookie(default=None),
# ):
#     if not q:
#         return last_query
#     return q


# @api_router_v1.post("/items/")
# async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
#     return {"q_or_cookie": query_or_default}
