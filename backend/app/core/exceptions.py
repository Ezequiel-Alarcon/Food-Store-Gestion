"""app.core.exceptions

Excepciones custom para el API que mapean errores de dominio a códigos HTTP
y que el middleware convierte a formato RFC 7807.

Ejemplos:
    raise NotFoundError("Usuario", user_id)
    raise ValidationError("Email inválido")
    raise UnauthorizedError("No autenticado")
"""

from __future__ import annotations


class AppError(Exception):
    """Base class para todas las excepciones de la aplicación."""

    status_code: int = 500
    title: str = "Internal Server Error"
    type_uri: str = "https://httpstatuses.com/500"

    def __init__(self, detail: str = "", *, instance: str = ""):
        self.detail = detail or self.title
        self.instance = instance
        super().__init__(self.detail)

    def to_problem_detail(self, debug: bool = False) -> dict:
        """Convierte la excepción a formato RFC 7807."""
        result = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status_code,
            "detail": self.detail,
            "instance": self.instance,
        }
        return result


class NotFoundError(AppError):
    """Recurso no encontrado. HTTP 404."""

    status_code = 404
    title = "Not Found"
    type_uri = "https://httpstatuses.com/404"

    def __init__(self, resource: str, resource_id: str | int, *, instance: str = ""):
        detail = f"{resource} with id {resource_id} not found"
        super().__init__(detail, instance=instance)


class ValidationError(AppError):
    """Error de validación en inputs. HTTP 422."""

    status_code = 422
    title = "Validation Error"
    type_uri = "https://httpstatuses.com/422"


class UnauthorizedError(AppError):
    """No autenticado. HTTP 401."""

    status_code = 401
    title = "Unauthorized"
    type_uri = "https://httpstatuses.com/401"

    def __init__(self, detail: str = "Authentication required", *, instance: str = ""):
        super().__init__(detail, instance=instance)


class ForbiddenError(AppError):
    """No autorizado para este recurso. HTTP 403."""

    status_code = 403
    title = "Forbidden"
    type_uri = "https://httpstatuses.com/403"

    def __init__(self, detail: str = "Access denied", *, instance: str = ""):
        super().__init__(detail, instance=instance)


class ConflictError(AppError):
    """Conflicto de estado (e.g., recurso ya existe). HTTP 409."""

    status_code = 409
    title = "Conflict"
    type_uri = "https://httpstatuses.com/409"


class RateLimitError(AppError):
    """Rate limit excedido. HTTP 429."""

    status_code = 429
    title = "Too Many Requests"
    type_uri = "https://httpstatuses.com/429"

    def __init__(self, detail: str = "Rate limit exceeded. Try again later.", *, instance: str = ""):
        super().__init__(detail, instance=instance)


class BadRequestError(AppError):
    """Request malformado. HTTP 400."""

    status_code = 400
    title = "Bad Request"
    type_uri = "https://httpstatuses.com/400"