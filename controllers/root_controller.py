from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/", tags=["Root"])

class RootController:
    @staticmethod
    @router.get("/", include_in_schema=False)
    def get_all_countries():
        return RedirectResponse(url="/docs")
