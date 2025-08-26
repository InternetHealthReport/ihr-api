import importlib
import pkgutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from controllers import __path__ as controllers_path
from dotenv import load_dotenv
import os

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
    version="v1.11",
    docs_url=None,
    redoc_url=None,
)

# Automatically import and register all routers inside "controllers"
for _, module_name, _ in pkgutil.iter_modules(controllers_path):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/docs", include_in_schema=False)
@app.get("/docs/", include_in_schema=False)
def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        get_swagger_ui_html={
            "defaultModelsExpandDepth": -1
        }
    )

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
