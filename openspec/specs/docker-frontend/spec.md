## ADDED Requirements

### Requirement: Frontend runs in a Docker container
The system SHALL provide a `Dockerfile` in `frontend/` that builds a containerized React + Vite application with Node.js 18.

#### Scenario: Frontend image builds successfully
- **WHEN** `docker build -t frontend:latest ./frontend` is executed
- **THEN** the image builds without errors and contains all npm dependencies from `package.json`

#### Scenario: Frontend dev server starts with hot reload
- **WHEN** the frontend container is built with `target: dev`
- **THEN** Vite dev server SHALL start on port 5173 and bind mounts SHALL be configured for live code updates

### Requirement: Frontend proxies API requests to backend
The system SHALL configure the Vite dev server proxy to forward `/api` requests to the backend service.

#### Scenario: API requests are proxied in Docker
- **WHEN** the frontend container runs within docker-compose and `VITE_BACKEND_URL` is set to `http://backend:8000`
- **THEN** all `/api/*` requests from the browser SHALL be forwarded to the backend container on port 8000

#### Scenario: API proxy falls back to localhost outside Docker
- **WHEN** `VITE_BACKEND_URL` is not set (running without Docker)
- **THEN** the proxy SHALL fall back to `http://localhost:8000`

### Requirement: Frontend supports dev and prod targets
The system SHALL use a multi-stage Dockerfile with `base` and `dev` targets, with `prod` structure documented as comments.

#### Scenario: Dev target serves with Vite
- **WHEN** the frontend container is built with `target: dev`
- **THEN** the application SHALL run `npm run dev` with `--host 0.0.0.0` to accept connections from outside the container

#### Scenario: Prod target structure is documented
- **WHEN** a developer reads the frontend `Dockerfile`
- **THEN** commented-out stages for `build` and `prod` (Nginx) SHALL be present with clear instructions for activation

### Requirement: Frontend excludes unnecessary files from build context
The system SHALL provide a `.dockerignore` file in `frontend/` that excludes `node_modules`, build output, and development artifacts.

#### Scenario: Build context is minimal
- **WHEN** `docker build ./frontend` is executed
- **THEN** the build context SHALL NOT include `node_modules`, `dist`, `.git`, `.env`, or IDE configuration files
