"""app.core.middleware

Middleware para manejo centralizado de errores RFC 7807.
"""

from __future__ import annotations

import sys
import traceback
from typing import Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import AppError

settings = get_settings()


class ErrorHandlerMiddleware:
    """Middleware que captura todas las excepciones y las convierte a RFC 7807."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Skip error handling for docs/openapi paths
        path = scope.get("path", "")
        if path in ("/docs", "/openapi.json", "/redoc", "/health"):
            await self.app(scope, receive, send)
            return

        # Process request through exception handlers
        response_started = False

        async def send_wrapper(status_code: int, headers: list[tuple], body: bytes):
            nonlocal response_started
            response_started = True
            await send({
                "type": "http.response.start",
                "status": status_code,
                "headers": headers,
            })
            await send({
                "type": "http.response.body",
                "body": body,
            })

        try:
            await self.app(scope, receive, send)
        except AppError as exc:
            if not response_started:
                problem = exc.to_problem_detail(debug=settings.DEBUG)
                status_code = exc.status_code
                await send_wrapper(
                    status_code,
                    [(b"content-type", b"application/problem+json")],
                    _json_bytes(problem),
                )
        except Exception as exc:
            if not response_started:
                # Log the full traceback
                exc_info = "".join(traceback.format_exception(*sys.exc_info()))
                # Log here (structured logging would be better in production)
                print(f"[ERROR] Unhandled exception: {exc}", file=sys.stderr)
                print(exc_info, file=sys.stderr)

                if settings.DEBUG:
                    problem = {
                        "type": "https://httpstatuses.com/500",
                        "title": "Internal Server Error",
                        "status": 500,
                        "detail": exc_info,
                        "instance": path,
                    }
                else:
                    problem = {
                        "type": "https://httpstatuses.com/500",
                        "title": "Internal Server Error",
                        "status": 500,
                        "detail": "An internal error occurred. Please try again later.",
                        "instance": path,
                    }

                await send_wrapper(
                    500,
                    [(b"content-type", b"application/problem+json")],
                    _json_bytes(problem),
                )


def _json_bytes(data: dict) -> bytes:
    """Serialize dict to JSON bytes."""
    import json
    return json.dumps(data).encode("utf-8")