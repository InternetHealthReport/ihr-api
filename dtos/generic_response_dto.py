from typing import TypeVar, List, Optional, Generic
from fastapi import Request
from urllib.parse import urlencode, urlunparse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import ast

try:
    load_dotenv()
except:
    pass

PROXY_PATH = os.getenv("PROXY_PATH")

# T is a generic type variable that will be replaced with a specific DTO type (e.g., CountryDTO) 
# when GenericResponseDTO is used (e.g GenericResponseDTO[CountryDTO] used in CountryController).
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
    scheme = request.headers.get("cf-visitor", request.url.scheme)
    if "scheme" in scheme:
        scheme = ast.literal_eval(scheme)["scheme"]
    else:
        scheme = request.url.scheme
    return urlunparse((
        scheme,
        request.url.netloc if PROXY_PATH is None else f"{request.url.netloc}/{PROXY_PATH}",
        request.url.path,
        "",
        urlencode(query_params),
        ""
    ))
