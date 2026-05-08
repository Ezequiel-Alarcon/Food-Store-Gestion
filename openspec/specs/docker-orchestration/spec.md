## ADDED Requirements

### Requirement: docker-compose orchestrates all services
The system SHALL provide a `docker-compose.yml` at the project root that defines and orchestrates the `db`, `backend`, and `frontend` services.

#### Scenario: All services start with a single command
- **WHEN** `docker compose up` is executed from the project root
- **THEN** all three services (db, backend, frontend) SHALL start and become healthy

#### Scenario: Backend depends on database health
- **WHEN** docker-compose starts services
- **THEN** the backend service SHALL NOT attempt to start until the db service passes its healthcheck

### Requirement: PostgreSQL data is persisted across restarts
The system SHALL use a Docker named volume for PostgreSQL data storage.

#### Scenario: Data survives container restart
- **WHEN** `docker compose down && docker compose up` is executed
- **THEN** all previously inserted data (users, roles, etc.) SHALL still be present in the database

#### Scenario: Volume is named and managed by Compose
- **WHEN** the `db` service is defined in docker-compose
- **THEN** a named volume `pg_data` SHALL be used for `/var/lib/postgresql/data`

### Requirement: Environment variables are centralized in root .env
The system SHALL use a single `.env` file at the project root for all Docker environment configuration.

#### Scenario: docker-compose reads variables from root .env
- **WHEN** `docker compose up` is executed
- **THEN** all environment variables defined in `.env` SHALL be available to all services

#### Scenario: Database connection uses service name
- **WHEN** the backend container connects to PostgreSQL
- **THEN** `DATABASE_URL` SHALL use `db` as the hostname (not `localhost`)

### Requirement: Services expose ports for local development
The system SHALL expose development ports to the host machine.

#### Scenario: Services are reachable on localhost
- **WHEN** all services are running via docker-compose
- **THEN** the frontend SHALL be reachable at `http://localhost:5173`, the backend at `http://localhost:8000`, and PostgreSQL at `localhost:5432`

### Requirement: Database has a healthcheck
The system SHALL define a healthcheck for the PostgreSQL service using `pg_isready`.

#### Scenario: Database healthcheck reports healthy
- **WHEN** PostgreSQL has started and is accepting connections
- **THEN** `pg_isready` SHALL return success and docker-compose SHALL mark the service as healthy

#### Scenario: Backend waits for database healthy status
- **WHEN** docker-compose orchestrates service startup
- **THEN** the backend SHALL wait for the db healthcheck to pass before starting, AND the backend entrypoint SHALL additionally verify connectivity before running migrations

### Requirement: Local development without Docker still works
The system SHALL preserve existing local development workflows.

#### Scenario: Backend runs outside Docker
- **WHEN** a developer runs `uvicorn app.main:app --reload` from the `backend/` directory with a local PostgreSQL
- **THEN** the application SHALL start and function identically to before this change

#### Scenario: Frontend runs outside Docker
- **WHEN** a developer runs `npm run dev` from the `frontend/` directory
- **THEN** Vite SHALL start and function identically to before this change
