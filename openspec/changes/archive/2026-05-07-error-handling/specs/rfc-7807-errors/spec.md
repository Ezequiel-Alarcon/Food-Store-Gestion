## ADDED Requirements

### Requirement: RFC 7807 Problem Details response format
All error responses from the API SHALL follow RFC 7807 (Problem Details for HTTP APIs) with the following fields:
- `type` (string): URI reference to the error type
- `title` (string): Short, human-readable summary of the problem
- `status` (integer): HTTP status code
- `detail` (string): Human-readable explanation specific to this occurrence
- `instance` (string): URI reference that identifies the specific occurrence

#### Scenario: Not found error returns RFC 7807 format
- **WHEN** a GET request is made to `/api/v1/productos/99999` and the resource does not exist
- **THEN** the response SHALL return HTTP 404 with body containing `{"type": "about:blank", "title": "Not Found", "status": 404, "detail": "Resource with id 99999 not found", "instance": "/api/v1/productos/99999"}`

#### Scenario: Validation error returns RFC 7807 format
- **WHEN** a POST request is made with invalid data to `/api/v1/auth/register`
- **THEN** the response SHALL return HTTP 422 with body containing RFC 7807 fields plus `errors` array with field-level validation errors

#### Scenario: Internal server error in development returns stack trace
- **WHEN** an unhandled exception occurs and `DEBUG=true`
- **THEN** the `detail` field SHALL contain the full stack trace for debugging

#### Scenario: Internal server error in production hides implementation details
- **WHEN** an unhandled exception occurs and `DEBUG=false`
- **THEN** the `detail` field SHALL contain a generic message and the stack trace SHALL be logged but not exposed to client

### Requirement: Custom exception classes
The system SHALL provide custom exception classes in `core/exceptions.py` that map domain errors to HTTP status codes:
- `NotFoundError`: HTTP 404
- `ValidationError`: HTTP 422
- `UnauthorizedError`: HTTP 401
- `ForbiddenError`: HTTP 403
- `ConflictError`: HTTP 409
- `RateLimitError`: HTTP 429

#### Scenario: Service raises NotFoundError
- **WHEN** a service layer raises `NotFoundError("User", user_id)`
- **THEN** the API SHALL return HTTP 404 with RFC 7807 body

### Requirement: Global error handler middleware
The system SHALL have an `ErrorHandlerMiddleware` that catches all unhandled exceptions and converts them to RFC 7807 responses.

#### Scenario: Unhandled exception is caught by middleware
- **WHEN** an unhandled `ValueError` occurs in a service
- **THEN** the middleware SHALL catch it and return HTTP 500 with RFC 7807 body

#### Scenario: HTTPException is converted to RFC 7807
- **WHEN** FastAPI raises an `HTTPException`
- **THEN** the middleware SHALL convert it to RFC 7807 format