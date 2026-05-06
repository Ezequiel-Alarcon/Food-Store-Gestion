## Context

Food Store is a full-stack e-commerce system that requires a clear separation of concerns between backend (FastAPI + SQLModel + PostgreSQL) and frontend (React + TypeScript + Vite). The codebase must support 18 sequential changes across 9+ sprints, each adding features incrementally. Without a solid foundational structure, subsequent changes risk inconsistency, naming conflicts, and architectural drift.

Current state: Monorepo directories `backend/` and `frontend/` exist at project root but are empty or minimally scaffolded.

## Goals / Non-Goals

**Goals:**
- Establish backend structure using **feature-first architecture**: `backend/app/modules/` for domain logic, `backend/app/core/` for cross-cutting patterns.
- Establish frontend structure using **Feature-Sliced Design (FSD)**: clear layer separation (app → pages → features → entities → shared) with unidirectional imports.
- Create standard configuration files (`.gitignore`, `README.md`, `.env.example`) to document conventions and reduce onboarding friction.
- Define placeholder files for dependency management (`requirements.txt`, `package.json`) to be populated in subsequent changes.
- Ensure directory structure reflects architectural decisions (Clean Architecture backend, FSD frontend).

**Non-Goals:**
- Implementing any feature code (auth, products, orders, etc.). This change is scaffolding only.
- Installing or configuring actual dependencies. That happens in `backend-config` and `frontend-config`.
- Creating database migrations. That happens in `backend-config`.
- Creating any React components or API endpoints. Structure only.

## Decisions

### D1: Feature-First Backend Organization (vs Layered-First)
**Decision**: Use feature-first module structure in `backend/app/modules/`. Each module (e.g., `auth/`, `productos/`, `pedidos/`) is self-contained with its own router, service, repository, schemas, and model.

**Rationale**: 
- Improves cohesion: related code lives together.
- Simplifies onboarding: new contributors find everything for a feature in one place.
- Reduces circular dependencies: modules don't import from each other.

**Alternative considered**: Layered-first (`backend/app/routers/`, `backend/app/services/`, `backend/app/models/`). Rejected because it spreads related code across multiple folders, increasing friction for feature-level changes.

### D2: Feature-Sliced Design for Frontend (vs Atomic Design)
**Decision**: Use FSD with explicit layer separation: `src/app/` (providers, routing), `src/pages/` (route definitions), `src/features/` (user interactions), `src/entities/` (domain models, API clients), `src/shared/` (UI components, utilities).

**Rationale**:
- Enforces unidirectional imports: features never import from pages or app.
- Reduces bundle size: features can be lazy-loaded.
- Scales better than atomic design for team-based feature development.

**Alternative considered**: Atomic design (`src/components/atoms/`, `src/components/molecules/`, etc.). Rejected because it encourages importing UI primitives across features, leading to tangled state management.

### D3: Core Folder for Cross-Cutting Patterns
**Decision**: Backend includes `backend/app/core/` for infrastructure code: database config, UoW implementation, BaseRepository, security utilities, custom exceptions, middleware.

**Rationale**:
- Centralizes patterns that all modules depend on.
- Prevents duplication of UoW, BaseRepository, etc.
- Clear separation: modules depend on core, not vice versa.

### D4: Git Ignore Strategy
**Decision**: Single `.gitignore` at project root that covers both backend and frontend (using patterns like `backend/.venv/`, `backend/__pycache__/`, `frontend/node_modules/`, etc.).

**Rationale**:
- Simpler to maintain than multiple `.gitignore` files.
- Standard practice in monorepos.

**Alternative considered**: Separate `.gitignore` per subdirectory. Rejected for simplicity.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Feature-first backend may lead to code duplication across modules | Enforce code reuse via core/ patterns (BaseRepository, UoW, shared utilities). Code review discipline. |
| FSD frontend may feel rigid initially | Document FSD layer rules in README and CONTRIBUTING guide. Start with clear examples. |
| Over-scaffolding unused directories | Accept it. Better to have empty placeholders than discover missing structure mid-implementation. |
| Team members unfamiliar with FSD or feature-first | Include architecture diagrams in README. Link to SDD onboarding docs. |

## Migration Plan

1. Create directory structure (no code changes).
2. Commit scaffold with git.
3. Subsequent changes (backend-config, frontend-config) populate dependencies and core files.

No rollback needed — this is pre-implementation.

## Open Questions

- Should backend modules be grouped further by domain (e.g., `modules/catalog/`, `modules/orders/`)? **Decision**: No, keep flat. Changes 8-10 cover catalog; changes 13-18 cover orders. Flat structure avoids premature organizational depth.
- Should frontend include an `api/` folder at root or within `entities/`? **Decision**: Keep API clients within `entities/` to maintain FSD separation.
