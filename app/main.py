import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.cors_origins
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
