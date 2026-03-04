"""Schema definitions for structured error responses in the FastAPI application."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    """Error detail structure for consistent error responses."""

    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Error response model for consistent API error responses."""

    error: ErrorDetail

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "The requested item was not found.",
                    "details": {"resource": "Item", "resource_id": 123},
                }
            }
        }
    )
