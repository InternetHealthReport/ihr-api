import importlib
import pkgutil
from fastapi import FastAPI
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

**For bulk downloads please use: [https://ihr-archive.iijlab.net/](https://ihr-archive.iijlab.net/)**

Parameters ending with __lte and __gte (acronyms for 'less than or equal to', and, 'greater than or equal to') are used for selecting a range of values.

[Contact the developers](mailto:admin@ihr.live)

[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""

# The base URL of the app
app = FastAPI(
    root_path="" if PROXY_PATH is None else f"/{PROXY_PATH}",
    title="IHR API",
    description=description,
    version="v1.0",
    redoc_url=None
)

# Automatically import and register all routers inside "controllers"
for _, module_name, _ in pkgutil.iter_modules(controllers_path):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
