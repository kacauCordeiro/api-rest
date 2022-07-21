# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.timing import add_timing_middleware
from app.apidocs.openapi import api_openapi
from fastapi.openapi.utils import get_openapi
from app.routes.fastapi_v1 import api_router_v1


def create_app():
    """create_app function."""
    app = FastAPI(
        docs_url="/apidocs", redoc_url="/v1/documentation", openapi_url="/v1/futebol-openapi.json"
    )
    add_timing_middleware(app, record="", prefix="app", exclude="")

    @app.get("/")
    async def _index():
        """Exibe Api."""
        return JSONResponse(content={"status": 200, "message": "api-rest-futebol v1.0"})

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        return api_openapi()

    app.openapi = custom_openapi

    app.include_router(api_router_v1, prefix="/v1")
    return app
