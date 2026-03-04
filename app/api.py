"""This module defines the API routes for the FastAPI application."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
)

router = APIRouter()


class ItemCreate(BaseModel):
    """Example item model for demonstration purposes."""

    name: str = Field(..., min_length=1)
    description: str | None = None
    quantity: int = Field(..., ge=1)


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint that returns a simple message."""
    return {
        "message": "Welcome to the FastAPI application! Please visit /docs for API documentation."
    }


@router.get("/error/not-found")
async def trigger_not_found() -> None:
    """Endpoint to trigger NotFoundError."""
    raise NotFoundError(resource="Item", resource_id=123)


@router.post("/error/validation/item")
async def trigger_validation_item(item: ItemCreate) -> dict[str, str | ItemCreate]:
    """Endpoint to trigger validation error using ItemCreate schema."""
    return {"message": "Item is valid", "item": item}


@router.get("/error/authentication")
async def trigger_authentication() -> None:
    """Endpoint to trigger AuthenticationError."""
    raise AuthenticationError()


@router.get("/error/authorization")
async def trigger_authorization() -> None:
    """Endpoint to trigger AuthorizationError."""
    raise AuthorizationError(action="delete", resource="Item")


@router.get("/error/conflict")
async def trigger_conflict() -> None:
    """Endpoint to trigger ConflictError."""
    raise ConflictError(resource="Item")


@router.get("/error/external-service")
async def trigger_external_service() -> None:
    """Endpoint to trigger ExternalServiceError."""
    raise ExternalServiceError(service="PaymentGateway")


@router.get("/error/http")
async def trigger_http_error() -> None:
    """Endpoint to trigger a generic HTTPException."""
    raise HTTPException(status_code=400, detail="Bad request triggered")


@router.get("/error/unhandled")
async def trigger_unhandled() -> None:
    """Endpoint to trigger an unhandled exception."""
    raise ValueError("This is an unhandled exception for testing purposes")
