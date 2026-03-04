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
from app.schemas import ErrorResponse

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


@router.get(
    "/error/not-found", responses={404: {"model": ErrorResponse, "description": "Item not found"}}
)
async def trigger_not_found() -> None:
    """Endpoint to trigger NotFoundError."""
    raise NotFoundError(resource="Item", resource_id=123)


@router.post(
    "/error/validation/item",
    responses={422: {"model": ErrorResponse, "description": "Validation error"}},
)
async def trigger_validation_item(item: ItemCreate) -> dict[str, str | ItemCreate]:
    """Endpoint to trigger validation error using ItemCreate schema."""
    return {"message": "Item is valid", "item": item}


@router.get(
    "/error/authentication",
    responses={401: {"model": ErrorResponse, "description": "Authentication required"}},
)
async def trigger_authentication() -> None:
    """Endpoint to trigger AuthenticationError."""
    raise AuthenticationError()


@router.get(
    "/error/authorization",
    responses={403: {"model": ErrorResponse, "description": "Authorization required"}},
)
async def trigger_authorization() -> None:
    """Endpoint to trigger AuthorizationError."""
    raise AuthorizationError(action="delete", resource="Item")


@router.get(
    "/error/conflict", responses={409: {"model": ErrorResponse, "description": "Conflict error"}}
)
async def trigger_conflict() -> None:
    """Endpoint to trigger ConflictError."""
    raise ConflictError(resource="Item")


@router.get(
    "/error/external-service",
    responses={502: {"model": ErrorResponse, "description": "External service error"}},
)
async def trigger_external_service() -> None:
    """Endpoint to trigger ExternalServiceError."""
    raise ExternalServiceError(service="PaymentGateway")


@router.get("/error/http", responses={400: {"model": ErrorResponse, "description": "Bad request"}})
async def trigger_http_error() -> None:
    """Endpoint to trigger a generic HTTPException."""
    raise HTTPException(status_code=400, detail="Bad request triggered")


@router.get(
    "/error/unhandled", responses={500: {"model": ErrorResponse, "description": "Unhandled error"}}
)
async def trigger_unhandled() -> None:
    """Endpoint to trigger an unhandled exception."""
    raise ValueError("This is an unhandled exception for testing purposes")
