import importlib
import pkgutil
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from controllers import __path__ as controllers_path
from dotenv import load_dotenv
import os
from starlette.routing import Match
import time
import logging
from sqlalchemy.exc import OperationalError

try:
    load_dotenv()
except:
    pass

PROXY_PATH = os.getenv("PROXY_PATH")

description = f"""
```[ Base URL: {'www.ihr.live' if PROXY_PATH is None else f'www.ihr.live/{PROXY_PATH}'} ]```

This RESTful API is intended for developers and researchers integrating IHR data to their workflow. API data is also available via our [Python library](https://www.ihr.live/ihr/en-us/documentation#Python_Library).

**For bulk downloads please use: [https://archive.ihr.live/](https://archive.ihr.live/)**

Parameters ending with __lte and __gte (acronyms for 'less than or equal to', and, 'greater than or equal to') are used for selecting a range of values.

[Contact the developers](mailto:admin@ihr.live)

[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""

# Silence uvicorn's built-in access logger — and leave it alone
uv_access = logging.getLogger("uvicorn.access")
uv_access.handlers[:] = []
uv_access.propagate = False
uv_access.setLevel(logging.WARNING)

# Use your OWN logger name, not "uvicorn.access"
logger = logging.getLogger("ihr.access")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False  # prevent bubbling up to the root logger

# The base URL of the app
app = FastAPI(
    root_path="" if PROXY_PATH is None else f"/{PROXY_PATH}",
    title="IHR API",
    description=description,
    version="v2.2",
    redoc_url=None,
    swagger_ui_parameters={ "defaultModelsExpandDepth": -1 },
)

@app.middleware("http")
async def reject_unknown_query_params(request: Request, call_next):
    scope = request.scope
    allowed_params = None
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        # Use Starlette's own matching — handles path params, methods, everything
        match, _ = route.matches(scope)
        if match == Match.FULL:
            allowed_params = {p.name for p in route.dependant.query_params}
            break
    if allowed_params is not None:
        extra = set(request.query_params.keys()) - allowed_params
        if extra:
            return JSONResponse(
                {
                    "error": "invalid_query_params",
                    "unexpected": sorted(extra),
                    "allowed": sorted(allowed_params),
                },
                status_code=400,
            )
    return await call_next(request)

@app.middleware("http")
async def access_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        raise
    finally:
        duration_s = time.perf_counter() - start
        client = request.client.host if request.client else "unknown"
        path = request.url.path + ("?" + str(request.url.query) if request.url.query else "")
        msg = '%s - "%s %s" %s %.3fs', client, request.method, path, status, duration_s
        if status >= 500:
            logger.error(*msg)
        elif status >= 400:
            logger.warning(*msg)
        else:
            logger.info(*msg)
    return response

async def db_error_handler(request: Request, exc: OperationalError):
    if getattr(exc.orig, "pgcode", None) == "57014":  # 57014 = query_canceled
        return JSONResponse({"error": "query_timeout", "message": "The request took too long"}, status_code=504)
    return JSONResponse({"error": "database_error"}, status_code=500)

app.add_exception_handler(OperationalError, db_error_handler)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# Automatically import and register all routers inside "controllers"
for _, module_name, _ in pkgutil.iter_modules(controllers_path):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

origins = [
    "http://localhost:5173",
    "http://www.ihr.live",
    "https://www.ihr.live"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)