"""Manipula o openapi.json."""
import json
import os
from typing import List


class OpenApi:
    """Carrega e modifica o openapi."""

    def __init__(self, openapi_path: str) -> None:
        """Carrega e modifica um openapi json.

        Args:
            openapi (str): caminho do arquivo openapi
        """
        with open(openapi_path, mode="r", encoding="utf-8") as openapi_json:
            self.__openapi = json.load(openapi_json)

    def filter_server(self, server: str):
        """Mantem apenas o servidor informado da lista de "servers".

        Args:
            server (str): dominio do servidor
        """
        filtered = [s for s in self.__openapi["servers"] if server in s["url"]]
        if filtered:
            self.__openapi["servers"] = filtered

    def exclude_endpoints(self, paths: List[str]):
        """Remove os endpoints indesejados ou inativos.

        Args:
            paths (List[str]): Lista de endpoints
        """
        filtered = dict((k, v) for k, v in self.__openapi["paths"].items() if k not in paths)
        self.__openapi["paths"] = filtered if filtered else {}

    def get(self) -> dict:
        """Retorna o arquivo openapi em formato de dict.

        Returns:
            dict: openapi
        """
        return self.__openapi


def api_openapi() -> dict:
    """Retorna o openapi que sera carregado Swagger/Redocs/Openapi.json."""
    openapi = OpenApi("app/apidocs/futebol-openapi.json")
    openapi.exclude_endpoints(["/v1/"])
    return openapi.get()
