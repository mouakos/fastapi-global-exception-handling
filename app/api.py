"""This module defines the API routes for the FastAPI application."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint that returns a simple message."""
    return {
        "message": "Welcome to the FastAPI application! Please visit /docs for API documentation."
    }
