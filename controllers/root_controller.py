from fastapi import APIRouter
from fastapi.responses import RedirectResponse
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
    @router.get("", include_in_schema=False)
    @router.get("/", include_in_schema=False)
    def get_root():
        return RedirectResponse(url="/docs" if PROXY_PATH is None else f"/{PROXY_PATH}/docs")
