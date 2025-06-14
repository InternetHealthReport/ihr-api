import importlib
import pkgutil
from fastapi import FastAPI
from controllers import __path__ as controllers_path  # Adjusted for `ihr` structure

# The base URL of the app
app = FastAPI()

# Automatically import and register all routers inside "ihr/controllers"
for _, module_name, _ in pkgutil.iter_modules(controllers_path):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
