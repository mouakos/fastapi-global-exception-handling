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

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ItemCreate(BaseModel):
    """Request body for item creation."""

    name: str = Field(..., min_length=1)
    description: str | None = None
    quantity: int = Field(..., ge=1)


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

router = APIRouter()


@router.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Root endpoint — returns a welcome message."""
    return {
        "message": "Welcome to the FastAPI application! Please visit /docs for API documentation."
    }


# ---------------------------------------------------------------------------
# Error simulation router
# ---------------------------------------------------------------------------

error_router = APIRouter(prefix="/error", tags=["Error Simulation"])


@error_router.get(
    "/not-found",
    responses={404: {"model": ErrorResponse, "description": "Resource not found"}},
)
async def trigger_not_found() -> None:
    """Simulate a 404 NotFoundError raised when fetching a missing resource."""
    raise NotFoundError(resource="Item", resource_id=123)


@error_router.get(
    "/authentication",
    responses={401: {"model": ErrorResponse, "description": "Authentication required"}},
)
async def trigger_authentication() -> None:
    """Simulate a 401 AuthenticationError raised when credentials are missing or invalid."""
    raise AuthenticationError()


@error_router.get(
    "/authorization",
    responses={403: {"model": ErrorResponse, "description": "Permission denied"}},
)
async def trigger_authorization() -> None:
    """Simulate a 403 AuthorizationError raised when the caller lacks permission."""
    raise AuthorizationError(action="delete", resource="Item")


@error_router.post(
    "/validation/item",
    responses={422: {"model": ErrorResponse, "description": "Request validation failed"}},
)
async def trigger_validation_item(item: ItemCreate) -> dict[str, str | ItemCreate]:
    """Simulate a 422 validation error by submitting an invalid request body."""
    return {"message": "Item is valid", "item": item}


@error_router.post(
    "/conflict",
    responses={409: {"model": ErrorResponse, "description": "Resource conflict"}},
)
async def trigger_conflict() -> None:
    """Simulate a 409 ConflictError raised when creating a duplicate resource."""
    raise ConflictError(resource="Item")


@error_router.post(
    "/external-service",
    responses={502: {"model": ErrorResponse, "description": "External service failure"}},
)
async def trigger_external_service() -> None:
    """Simulate a 502 ExternalServiceError raised when a downstream service fails."""
    raise ExternalServiceError(service="PaymentGateway")


@error_router.get(
    "/http",
    responses={400: {"model": ErrorResponse, "description": "Bad request"}},
)
async def trigger_http_error() -> None:
    """Simulate a generic 400 HTTPException."""
    raise HTTPException(status_code=400, detail="Bad request triggered")


@error_router.get(
    "/unhandled",
    responses={500: {"model": ErrorResponse, "description": "Unhandled server error"}},
)
async def trigger_unhandled() -> None:
    """Simulate an unhandled exception caught by the global catch-all handler."""
    raise ValueError("This is an unhandled exception for testing purposes")


# Register the error simulation sub-router
router.include_router(error_router)
