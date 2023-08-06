import os
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import orjson


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)


def set_app_doc_static_file(app, favicon_url="icon.png"):
    """
    favicon_url :str: "icon.png" or "icon-yuanian.png"
    """
    root = os.path.dirname(os.path.realpath(__file__))
    app.mount("/static", StaticFiles(directory=f"{root}/static"), name="static")

    @app.get('/docs', include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
            swagger_favicon_url=f"/static/{favicon_url}",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
            redoc_favicon_url=f"/static/{favicon_url}",
        )

    @app.get("/8dbd28457ff989b4568a.worker.js.map", include_in_schema=False)
    async def redoc_worker_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - worker.js.map",
            redoc_js_url="/static/8dbd28457ff989b4568a.worker.js.map ",
        )


def create_app(title, version='0.0.1', openapi_tags=None, favicon_url='icon.png'):
    if openapi_tags is None:
        openapi_tags = [
            {"name": "private",
             "description": "私有接口"},
            {"name": "public",
             "description": "公有接口"},
        ]
    app = FastAPI(openapi_tags=openapi_tags,
                  title=title,
                  version=version,
                  description="",
                  docs_url=None,
                  redoc_url=None,
                  default_response_class=ORJSONResponse,
                  )
    set_app_doc_static_file(app, favicon_url=favicon_url)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def add_router(app: FastAPI, router:APIRouter):
    app.include_router(router)
