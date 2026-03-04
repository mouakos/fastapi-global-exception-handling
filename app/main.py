"""This is the main entry point for the FastAPI application."""

from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from loguru import logger

from app.api import router
from app.exception_handlers import register_exception_handlers
from app.logging import setup_logging

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
setup_logging(["uvicorn.access"])


# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Lifespan context manager to perform startup and shutdown tasks."""
    # Perform any additional startup tasks here (e.g. warmup, preloading) if needed
    yield
    await logger.complete()  # Ensure all logs are flushed on shutdown


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
