from fastapi import FastAPI

from .config import settings
from .database import init_db
from .routers import router

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
