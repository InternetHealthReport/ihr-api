from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import load_dotenv
import os

try:
    load_dotenv()
except:
    pass

PROXY_PATH = os.getenv("PROXY_PATH")

router = APIRouter(prefix="", tags=["Root"])

class RootController:
    @staticmethod
    @router.get("/", include_in_schema=False)
    def get_root():
        return RedirectResponse(url="/docs" if PROXY_PATH is None else f"/{PROXY_PATH}/docs")
    
    @staticmethod
    @router.get("/docs", include_in_schema=False)
    @router.get("/docs/", include_in_schema=False)
    def get_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=router.openapi_url,
            title=router.title,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

