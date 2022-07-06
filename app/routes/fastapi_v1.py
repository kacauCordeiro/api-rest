from fastapi import APIRouter, Query, Request
from pyparsing import Optional

from app.controllers.time_controller import TimeController
from app.controllers.jogador_controller import JogadorController
from app.controllers.transferencia_controller import TransferenciaController
from app.controllers.torneio_controller import TorneioController
from app.controllers.partidas_controller import PartidasController
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
    
# DELETE
@api_router_v1.delete("/time/{id}")
async def time(id: int = 0):
    """Enpoint para cadastrar time."""
    with MySQLConnection() as database:
        return TimeController(database).delete_time(id)

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

# GET
@api_router_v1.get("/times/{id}")
async def jogador_by_id(id: int = 0):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_times(id)
    
@api_router_v1.get("/jogadores/{id}")
async def jogadores(id: int = 0):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores()
    
@api_router_v1.get("/transferencias/{id}")
async def jogador_by_name(name: str = None):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores(name)

@api_router_v1.get("/torneios/{id}")
async def jogador_by_name(name: str = None):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores(name)

#UPDATE

#EVENTOS
@api_router_v1.get("/torneio/partida/{id}/inicio")
async def partida_inicio(id: int = 0):
    """Enpoint que cria o evento de inicio da partida."""
    with MySQLConnection() as database:
        return EventosController(database).evento_inicio(id)

