"""Global exception handlers for the FastAPI application."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import AppError
from app.schemas import ErrorResponse
from app.utils import get_request_info

# Mapping of common HTTP status codes to standardized error codes for consistent API responses
HTTP_ERROR_CODE_MAP: dict[int, str] = {
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

ErrorLevel = Literal["INFO", "ERROR", "EXCEPTION"]


def build_error_response(
    error_code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> ErrorResponse:
    """Create a consistent error content structure as ErrorResponse."""
    content: dict[str, Any] = {
        "error": {
            "code": error_code,
            "message": message,
        },
    }
    if details:
        content["error"]["details"] = details
    return ErrorResponse(**content)


def log_and_build_response(
    *,
    request: Request,
    status_code: int,
    event: str,
    error_code: str,
    message: str,
    details: dict[str, Any] | None = None,
    level: ErrorLevel = "INFO",
) -> JSONResponse:
    """Log the error event and build a JSONResponse with consistent structure."""
    response_model = build_error_response(error_code, message, details)
    request_info = get_request_info(request)
    bound = logger.bind(
        **asdict(request_info),
        status_code=status_code,
        **response_model.model_dump(exclude_none=True),
    )
    if level == "EXCEPTION":
        bound.exception(event)
    elif level == "ERROR":
        bound.error(event)
    else:
        bound.info(event)
    return JSONResponse(
        status_code=status_code, content=response_model.model_dump(exclude_none=True)
    )


def normalize_validation_errors(exc: RequestValidationError) -> list[dict[str, str]]:
    """Normalize Pydantic/FastAPI validation errors into API error shape."""
    errors: list[dict[str, str]] = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", ()))
        errors.append(
            {
                "field": field,
                "message": err.get("msg", "Invalid value"),
                "type": err.get("type", "value_error"),
            }
        )
    return errors


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the FastAPI application."""

    @app.exception_handler(AppError)
    async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
        """Handle all custom application exceptions."""
        return log_and_build_response(
            request=request,
            status_code=exc.status_code,
            event="application_error",
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            level="INFO" if exc.status_code < 500 else "ERROR",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        return log_and_build_response(
            request=request,
            status_code=422,
            event="validation_error",
            error_code="INVALID_INPUT",
            message="Request validation failed",
            details={"errors": normalize_validation_errors(exc)},
            level="INFO",
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle standard HTTP exceptions raised by FastAPI or Starlette."""
        error_code = HTTP_ERROR_CODE_MAP.get(exc.status_code, "HTTP_ERROR")
        return log_and_build_response(
            request=request,
            status_code=exc.status_code,
            event="http_error",
            error_code=error_code,
            message=str(exc.detail),
            level="INFO" if exc.status_code < 500 else "ERROR",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, _: Exception) -> JSONResponse:
        """Catch-all handler for unexpected errors."""
        return log_and_build_response(
            request=request,
            status_code=500,
            event="unhandled_exception",
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            level="EXCEPTION",
        )
