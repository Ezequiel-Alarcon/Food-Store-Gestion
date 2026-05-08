## ADDED Requirements

### Requirement: Backend runs in a Docker container
The system SHALL provide a `Dockerfile` in `backend/` that builds a containerized FastAPI application with Python 3.11.

#### Scenario: Backend image builds successfully
- **WHEN** `docker build -t backend:latest ./backend` is executed
- **THEN** the image builds without errors and contains all Python dependencies from `requirements.txt`

#### Scenario: Backend starts after database is ready
- **WHEN** the backend container starts and PostgreSQL is not yet accepting connections
- **THEN** the entrypoint SHALL retry the connection every 2 seconds until PostgreSQL is reachable, then proceed

#### Scenario: Backend waits for PostgreSQL timeout
- **WHEN** the backend container starts and PostgreSQL is unreachable for more than 60 seconds
- **THEN** the entrypoint SHALL exit with a non-zero status code and an error message

### Requirement: Backend runs migrations and seed on startup
The system SHALL execute Alembic migrations and seed data automatically before starting the application server.

#### Scenario: Migrations run successfully before server starts
- **WHEN** the backend container starts and PostgreSQL is ready
- **THEN** `alembic upgrade head` SHALL execute all pending migrations without errors

#### Scenario: Seed data is populated after migrations
- **WHEN** migrations complete successfully
- **THEN** `python -m app.db.seed` SHALL run and insert initial data (roles, estados, formas de pago, admin user) if not already present

#### Scenario: Seed is idempotent on restart
- **WHEN** the backend container restarts and seed data already exists in the database
- **THEN** the seed script SHALL detect existing records and skip insertion without errors

### Requirement: Backend supports dev and prod targets
The system SHALL use a multi-stage Dockerfile with `base`, `dev`, and `prod` targets.

#### Scenario: Dev target enables hot reload
- **WHEN** the backend container is built with `target: dev`
- **THEN** uvicorn SHALL start with `--reload` flag and bind-mount volumes SHALL be configured for live code updates

#### Scenario: Prod target uses production server
- **WHEN** the backend container is built with `target: prod`
- **THEN** the application SHALL run with Gunicorn + Uvicorn workers without debug mode or hot reload

### Requirement: Backend container receives shutdown signals correctly
The system SHALL ensure the backend process is PID 1 and handles SIGTERM for graceful shutdown.

#### Scenario: Graceful shutdown on docker stop
- **WHEN** `docker stop` is issued against the backend container
- **THEN** the application SHALL shut down within 10 seconds without data loss or corruption

### Requirement: Backend excludes unnecessary files from build context
The system SHALL provide a `.dockerignore` file in `backend/` that excludes virtual environments, cache files, and development artifacts.

#### Scenario: Build context is minimal
- **WHEN** `docker build ./backend` is executed
- **THEN** the build context SHALL NOT include `.venv`, `__pycache__`, `.git`, `*.pyc`, `.env`, or IDE configuration files
