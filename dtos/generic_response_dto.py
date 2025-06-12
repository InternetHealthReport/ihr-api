from typing import TypeVar, List, Optional, Generic
from fastapi import Request
from urllib.parse import urlencode, urlunparse
from pydantic import BaseModel

T = TypeVar("T")

# The generic response format returned by all endpoints
class GenericResponseDTO(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]

# Builds the url returned by "next" and "previous" fields in the GenericResponseDTO
def build_url(request: Request, page: Optional[int]) -> Optional[str]:
    if page is None:
        return None
    query_params = dict(request.query_params)
    query_params["page"] = str(page)
    return urlunparse((
        request.url.scheme,
        request.url.netloc,
        request.url.path,
        "",
        urlencode(query_params),
        ""
    ))
