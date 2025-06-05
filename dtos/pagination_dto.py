from typing import Optional
from fastapi import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    ordering: Optional[str] = Query(None, description="Field to order by")
