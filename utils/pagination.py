from typing import TypeVar, List, Optional, Callable, Generic, Any
from fastapi import Request
from urllib.parse import urlencode, urlunparse
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]


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

def paginate_and_order(
    items: List[Any],
    request: Request,
    page: int,
    order_by: Optional[Callable[[Any], Any]] = None
) -> PaginatedResponse:
    # If order_by is provided, but is not callable (i.e., it's a string), convert it to a callable
    if order_by:
        if not callable(order_by):
            # Assume order_by is the attribute name to sort by.
            order_field = order_by
            order_by = lambda x: getattr(x, order_field)
        items = sorted(items, key=order_by)
    total_count = len(items)
    page_size = 5
    offset = (page - 1) * page_size
    paginated_items = items[offset : offset + page_size]
    next_page = page + 1 if offset + page_size < total_count else None
    prev_page = page - 1 if page > 1 else None

    return PaginatedResponse(
        count=total_count,
        next=build_url(request, next_page),
        previous=build_url(request, prev_page),
        results=paginated_items
    )
