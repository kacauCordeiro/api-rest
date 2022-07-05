from fastapi import APIRouter, Query, Request
from pyparsing import Optional

from app.controllers.time_controller import TimeController
from app.controllers.jogador_controller import JogadorController
from app.controllers.transferencia_controller import TransferenciaController
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
async def contract(request: Request):
    """Enpoint para cadastrar transferencia."""
    with MySQLConnection() as database:
        body = await request.json()
        return TransferenciaController(database).insert_transferencia(body)

# GET
    
@api_router_v1.get("/jogadores")
async def jogadores():
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores()

@api_router_v1.get("/jogador_by_id")
async def jogador_by_id(id: int = 0):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores(id)
    
@api_router_v1.get("/jogador_by_name")
async def jogador_by_name(name: str = None):
    """Enpoint para listar todos os jogadores."""
    with MySQLConnection() as database:
        return JogadorController(database).list_jogadores(name)