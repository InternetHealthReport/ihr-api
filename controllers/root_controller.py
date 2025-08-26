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
    @router.get("/", include_in_schema=False, redirect_slashes=True)
    def get_all_countries():
        return RedirectResponse(url="/docs" if PROXY_PATH is None else f"/{PROXY_PATH}/docs")
