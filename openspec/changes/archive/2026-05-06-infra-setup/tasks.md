## 1. Backend Structure — Core

- [x] 1.1 Create `backend/app/` directory structure
- [x] 1.2 Create `backend/app/core/` for infrastructure (config, database, security, UoW)
- [x] 1.3 Create `backend/app/__init__.py` (empty or version marker)
- [x] 1.4 Create `backend/app/core/__init__.py`

## 2. Backend Structure — Modules

- [x] 2.1 Create `backend/app/modules/` directory
- [x] 2.2 Create `backend/app/modules/auth/` with `__init__.py`, `model.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`
- [x] 2.3 Create `backend/app/modules/usuarios/` with placeholder structure
- [x] 2.4 Create `backend/app/modules/direcciones/` with placeholder structure
- [x] 2.5 Create `backend/app/modules/categorias/` with placeholder structure
- [x] 2.6 Create `backend/app/modules/ingredientes/` with placeholder structure
- [x] 2.7 Create `backend/app/modules/productos/` with placeholder structure
- [x] 2.8 Create `backend/app/modules/pedidos/` with placeholder structure
- [x] 2.9 Create `backend/app/modules/pagos/` with placeholder structure
- [x] 2.10 Create `backend/app/modules/admin/` with placeholder structure
- [x] 2.11 Create `backend/app/modules/refreshtokens/` with placeholder structure

## 3. Backend Configuration Files

- [x] 3.1 Create `backend/requirements.txt` (placeholder for dependencies)
- [x] 3.2 Create `backend/.env.example` with placeholders for DATABASE_URL, SECRET_KEY, etc.
- [x] 3.3 Create `backend/README.md` documenting backend setup and architecture

## 4. Frontend Structure — Layers

- [x] 4.1 Create `frontend/src/app/` for app-level providers and routing config
- [x] 4.2 Create `frontend/src/pages/` for page/route definitions
- [x] 4.3 Create `frontend/src/features/` for feature modules (auth, cart, orders, admin)
- [x] 4.4 Create `frontend/src/entities/` for domain models and API clients
- [x] 4.5 Create `frontend/src/shared/` for UI components and shared utilities

## 5. Frontend Feature Directories

- [x] 5.1 Create `frontend/src/features/auth/` with placeholder structure (forms, hooks, guards)
- [x] 5.2 Create `frontend/src/features/cart/` with placeholder structure
- [x] 5.3 Create `frontend/src/features/orders/` with placeholder structure
- [x] 5.4 Create `frontend/src/features/admin/` with placeholder structure

## 6. Frontend Shared Directories

- [x] 6.1 Create `frontend/src/shared/ui/` for UI components (Button, Input, Modal, etc.)
- [x] 6.2 Create `frontend/src/shared/lib/` for utilities (api.ts, hooks, constants)
- [x] 6.3 Create `frontend/src/shared/types/` for TypeScript types and interfaces

## 7. Frontend Configuration Files

- [x] 7.1 Create `frontend/.env.example` with VITE_API_URL placeholder
- [x] 7.2 Create `frontend/README.md` documenting frontend setup and architecture
- [x] 7.3 Create `frontend/package.json` skeleton (to be populated in frontend-config)

## 8. Root Level Configuration

- [x] 8.1 Create/update `.gitignore` at project root covering backend and frontend patterns
- [x] 8.2 Create/update root-level `README.md` documenting the monorepo structure and workflow
- [x] 8.3 Create `.env.example` at project root (optional, for shared config)

## 9. Verification and Documentation

- [x] 9.1 Verify all directories exist with correct hierarchy
- [x] 9.2 Verify all `__init__.py` files exist in Python packages
- [x] 9.3 Verify all placeholder files created
- [x] 9.4 Test git can track the structure (no empty directories lost)
- [x] 9.5 Create CONTRIBUTING.md documenting architectural rules and patterns
