import importlib
import pkgutil
from fastapi import FastAPI
from controllers import __path__ as controllers_path

proxy_path = "api-dev"

description = f"""
```[ Base URL: www.ihr.live/{proxy_path} ]```

This RESTful API is intended for developers and researchers integrating IHR data to their workflow. API data is also available via our [Python library](https://www.ihr.live/ihr/en-us/documentation#Python_Library).

**For bulk downloads please use: [https://ihr-archive.iijlab.net/](https://ihr-archive.iijlab.net/)**

Parameters ending with __lte and __gte (acronyms for 'less than or equal to', and, 'greater than or equal to') are used for selecting a range of values.

[Contact the developers](mailto:admin@ihr.live)

[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""

# The base URL of the app
app = FastAPI(
    title="IHR API",
    description=description,
    version="0.2",
    docs_url=f"/{proxy_path}/docs",
    openapi_url=f"/{proxy_path}/openapi.json",
    redoc_url=None
)

# Automatically import and register all routers inside "controllers"
for _, module_name, _ in pkgutil.iter_modules(controllers_path):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
