"""app.core.schemas

Schemas compartidos para toda la aplicación.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProblemDetail(BaseModel):
    """RFC 7807 Problem Details response body."""

    type: str = Field(
        default="about:blank",
        description="URI reference to the error type"
    )
    title: str = Field(
        description="Short, human-readable summary of the problem"
    )
    status: int = Field(
        description="HTTP status code"
    )
    detail: str = Field(
        description="Human-readable explanation specific to this occurrence"
    )
    instance: str = Field(
        default="",
        description="URI reference that identifies the specific occurrence"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "https://httpstatuses.com/404",
                "title": "Not Found",
                "status": 404,
                "detail": "User with id 123 not found",
                "instance": "/api/v1/usuarios/123"
            }
        }
    )


class ValidationErrorDetail(BaseModel):
    """Detail para errores de validación Pydantic."""

    loc: list[str] = Field(
        description="Location of the field that failed validation"
    )
    msg: str = Field(
        description="Error message"
    )
    type: str = Field(
        description="Error type"
    )


class ValidationProblemDetail(ProblemDetail):
    """RFC 7807 con errores de validación por campo."""

    errors: list[ValidationErrorDetail] = Field(
        default_factory=list,
        description="List of validation errors"
    )