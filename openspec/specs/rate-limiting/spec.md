## ADDED Requirements

### Requirement: Rate limiting by IP address for public endpoints
Public endpoints SHALL be rate-limited by source IP address using slowapi:
- Default limit: 60 requests per minute per IP
- Endpoints excluded: `/health`, `/docs`, `/openapi.json`

#### Scenario: Exceeded rate limit returns 429
- **WHEN** a client makes more than 60 requests in one minute from the same IP to `/api/v1/productos`
- **THEN** the 61st request SHALL return HTTP 429 with `Retry-After` header

#### Scenario: Health endpoint bypasses rate limiting
- **WHEN** a client makes 100 requests to `/health` in one minute
- **THEN** all requests SHALL succeed (no rate limiting applied)

### Requirement: Rate limiting by user for authenticated endpoints
Authenticated endpoints SHALL be rate-limited by user ID (from JWT):
- Default limit: 100 requests per minute per user
- Auth endpoints (login, register): 5 requests per minute per IP

#### Scenario: Auth endpoint rate limiting
- **WHEN** a client makes 6 failed login attempts in one minute from the same IP
- **THEN** the 7th attempt SHALL return HTTP 429

#### Scenario: Authenticated user exceeds rate limit
- **WHEN** an authenticated user makes more than 100 requests per minute to protected endpoints
- **THEN** the 101st request SHALL return HTTP 429

### Requirement: Rate limit configuration via environment variables
Rate limit values SHALL be configurable via environment variables:
- `RATE_LIMIT_PUBLIC`: requests per minute for public endpoints (default: 60)
- `RATE_LIMIT_AUTHENTICATED`: requests per minute for authenticated endpoints (default: 100)
- `RATE_LIMIT_AUTH`: requests per minute for auth endpoints per IP (default: 5)

#### Scenario: Custom rate limit is applied
- **WHEN** `RATE_LIMIT_PUBLIC=30` is set in environment
- **THEN** public endpoints SHALL allow only 30 requests per minute per IP