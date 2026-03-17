from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.debug import router as debug_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.db.session import init_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_database(get_settings())
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AllyVPN API", lifespan=lifespan)
    app.include_router(health_router)
    if settings.is_local:
        app.include_router(debug_router)
    return app


app = create_app()
