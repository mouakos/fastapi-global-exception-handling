"""This is the main entry point for the FastAPI application."""

from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title="FastAPI Monitoring and Observability",
    version="1.0.0",
    servers=[],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/",
    },
    contact={
        "name": "Stephane Mouako",
        "url": "https://github.com/mouakos",
    },
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok",
    },
)

# ---------------------------------------------------------------------------
# Exception handlers & routes
# ---------------------------------------------------------------------------
app.include_router(router)
