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

# The base URL of the app
app = FastAPI(
    root_path="" if PROXY_PATH is None else f"/{PROXY_PATH}",
    title="IHR API",
    description=description,
    version="v2.0",
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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/health", include_in_schema=False)
def health():
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