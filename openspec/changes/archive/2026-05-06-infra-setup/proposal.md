## Why

Food Store requires a robust, scalable monorepo structure that separates backend and frontend concerns while maintaining clear architectural patterns. This change establishes the foundational scaffolding needed for all subsequent feature development, ensuring consistency in code organization, naming conventions, and dependency management from day one.

## What Changes

- **Backend structure**: Feature-first organization with `backend/app/modules/` for domain modules (auth, usuarios, productos, etc.) and `backend/app/core/` for cross-cutting patterns (UoW, repository base, dependencies).
- **Frontend structure**: Feature-Sliced Design (FSD) with clear layer separation: `src/app/`, `src/pages/`, `src/features/`, `src/entities/`, `src/shared/`.
- **Project root files**: `.gitignore`, `README.md`, `.env.example` for both backend and frontend.
- **Configuration files**: `backend/requirements.txt`, `frontend/package.json` (placeholders for manual population in backend-config and frontend-config).

## Capabilities

### New Capabilities
- `monorepo-structure`: Establishes backend and frontend directory hierarchy following Clean Architecture (backend) and FSD (frontend) patterns.
- `project-scaffolding`: Creates foundational configuration files (.gitignore, README.md, .env templates).

### Modified Capabilities
<!-- No existing capabilities modified in this change. -->

## Impact

- Affects: Directory structure, project organization, initial Git ignore rules.
- All subsequent changes will inherit this structure.
- No breaking changes to APIs or data models (this is pre-implementation).
- Dependencies: None (this is Change #1).

## Trazabilidad

- **US-000** → scaffolding base
