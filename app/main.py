from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(api_router, prefix=settings.api_version_str)

if __name__ == "__main__":
    if settings.environment == "development":
        reload = True
    else:
        reload = False

    uvicorn.run(
        settings.app_run_name,
        host=settings.host,
        port=settings.api_port,
        reload=reload,
    )