"""Global exception handlers for the FastAPI application."""

import logging
import traceback
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import AppError

# Configure logging
logger = logging.getLogger(__name__)


def create_error_content(
    error_code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict:
    """Create a consistent error content structure as dict."""
    content = {
        "error": {
            "code": error_code,
            "message": message,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    }
    if details:
        content["error"]["details"] = details
    return content


async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle all custom application exceptions."""
    # Log the error with context
    logger.warning(
        f"Application error: {exc.error_code} - {exc.message}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "details": exc.details,
        },
    )

    content = create_error_content(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    # Extract validation error details
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"], "type": error["type"]})

    logger.warning(
        f"Validation error on {request.url.path}",
        extra={"errors": errors, "method": request.method},
    )

    content = create_error_content(
        error_code="INVALID_INPUT",
        message="Request validation failed",
        details={"errors": errors},
    )
    return JSONResponse(status_code=422, content=content)


async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions raised by FastAPI or Starlette."""
    # Map status codes to error codes
    error_code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "PERMISSION_DENIED",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        408: "REQUEST_TIMEOUT",
        409: "RESOURCE_CONFLICT",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
        504: "GATEWAY_TIMEOUT",
    }

    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")

    content = create_error_content(
        error_code=error_code,
        message=str(exc.detail),
    )
    return JSONResponse(status_code=exc.status_code, content=content)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected errors."""
    # Log the full traceback for debugging
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc(),
        },
    )

    # Return generic error to client, hiding internal details
    content = create_error_content(
        error_code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again later.",
    )
    return JSONResponse(status_code=500, content=content)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the FastAPI application."""
    app.add_exception_handler(AppError, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
