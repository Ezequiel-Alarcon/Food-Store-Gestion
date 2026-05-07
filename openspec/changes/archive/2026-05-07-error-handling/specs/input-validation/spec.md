## ADDED Requirements

### Requirement: Input validation in Pydantic schemas
All Create and Update schemas SHALL validate inputs using Pydantic Field validators:
- String fields SHALL be stripped of leading/trailing whitespace
- Email fields SHALL be validated against email format
- Phone fields SHALL be validated against E.164 format
- Numeric fields SHALL have min/max constraints where applicable

#### Scenario: Whitespace-only name is rejected
- **WHEN** a POST request sends `{"nombre": "   "}` to create a category
- **THEN** the schema SHALL reject it with a validation error "String field 'nombre' cannot be empty or whitespace only"

#### Scenario: Invalid email format is rejected
- **WHEN** a POST request sends `{"email": "not-an-email"}` to register
- **THEN** the schema SHALL reject it with HTTP 422 and validation error on `email` field

#### Scenario: Valid input passes validation
- **WHEN** a POST request sends valid data to create a user
- **THEN** the schema SHALL accept it and pass to service layer

### Requirement: SQL injection prevention via ORM parameters
All database queries SHALL use parameterized queries (SQLModel/SQLAlchemy ORM) to prevent SQL injection attacks. Raw SQL string concatenation is strictly prohibited.

#### Scenario: Malicious input in search query
- **WHEN** user searches with query `"; DROP TABLE users; --"`
- **THEN** the system SHALL treat it as literal string and return empty results, NOT execute the injected SQL

### Requirement: XSS prevention in string inputs
All string inputs SHALL be stored as-is but sanitized on output (HTML encoding). The API SHALL NOT reflect raw user input in responses without encoding.

#### Scenario: Script tag in product name
- **WHEN** a product is created with name `"<script>alert('xss')</script>"`
- **THEN** the API SHALL store it correctly but return it HTML-encoded when queried