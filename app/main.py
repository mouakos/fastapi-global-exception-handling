"""This is the main entry point for the FastAPI application."""

from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.api import router
from app.exception_handlers import register_exception_handlers
from app.logging import setup_json_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Lifespan context manager to perform startup and shutdown tasks."""
    setup_json_logging()
    yield


# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Global Exception Handling Example",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/",
    },
    contact={
        "name": "Stephane Mouako",
        "url": "https://github.com/mouakos",
    },
)

# ---------------------------------------------------------------------------
# Exception handlers & routes
# ---------------------------------------------------------------------------
register_exception_handlers(app)
app.include_router(router)
