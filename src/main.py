from fastapi import FastAPI

from .config import settings
from .routers import router
from .tools.init_database import init_db

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(router)


@app.get("/")
async def read_root():
    return {"swagger": "/docs#/"}


@app.on_event("startup")
async def startup():
    await init_db()
