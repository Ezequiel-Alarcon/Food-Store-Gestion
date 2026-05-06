## 1. Backend Structure — Core

- [ ] 1.1 Create `backend/app/` directory structure
- [ ] 1.2 Create `backend/app/core/` for infrastructure (config, database, security, UoW)
- [ ] 1.3 Create `backend/app/__init__.py` (empty or version marker)
- [ ] 1.4 Create `backend/app/core/__init__.py`

## 2. Backend Structure — Modules

- [ ] 2.1 Create `backend/app/modules/` directory
- [ ] 2.2 Create `backend/app/modules/auth/` with `__init__.py`, `model.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`
- [ ] 2.3 Create `backend/app/modules/usuarios/` with placeholder structure
- [ ] 2.4 Create `backend/app/modules/direcciones/` with placeholder structure
- [ ] 2.5 Create `backend/app/modules/categorias/` with placeholder structure
- [ ] 2.6 Create `backend/app/modules/ingredientes/` with placeholder structure
- [ ] 2.7 Create `backend/app/modules/productos/` with placeholder structure
- [ ] 2.8 Create `backend/app/modules/pedidos/` with placeholder structure
- [ ] 2.9 Create `backend/app/modules/pagos/` with placeholder structure
- [ ] 2.10 Create `backend/app/modules/admin/` with placeholder structure
- [ ] 2.11 Create `backend/app/modules/refreshtokens/` with placeholder structure

## 3. Backend Configuration Files

- [ ] 3.1 Create `backend/requirements.txt` (placeholder for dependencies)
- [ ] 3.2 Create `backend/.env.example` with placeholders for DATABASE_URL, SECRET_KEY, etc.
- [ ] 3.3 Create `backend/README.md` documenting backend setup and architecture

## 4. Frontend Structure — Layers

- [ ] 4.1 Create `frontend/src/app/` for app-level providers and routing config
- [ ] 4.2 Create `frontend/src/pages/` for page/route definitions
- [ ] 4.3 Create `frontend/src/features/` for feature modules (auth, cart, orders, admin)
- [ ] 4.4 Create `frontend/src/entities/` for domain models and API clients
- [ ] 4.5 Create `frontend/src/shared/` for UI components and shared utilities

## 5. Frontend Feature Directories

- [ ] 5.1 Create `frontend/src/features/auth/` with placeholder structure (forms, hooks, guards)
- [ ] 5.2 Create `frontend/src/features/cart/` with placeholder structure
- [ ] 5.3 Create `frontend/src/features/orders/` with placeholder structure
- [ ] 5.4 Create `frontend/src/features/admin/` with placeholder structure

## 6. Frontend Shared Directories

- [ ] 6.1 Create `frontend/src/shared/ui/` for UI components (Button, Input, Modal, etc.)
- [ ] 6.2 Create `frontend/src/shared/lib/` for utilities (api.ts, hooks, constants)
- [ ] 6.3 Create `frontend/src/shared/types/` for TypeScript types and interfaces

## 7. Frontend Configuration Files

- [ ] 7.1 Create `frontend/.env.example` with VITE_API_URL placeholder
- [ ] 7.2 Create `frontend/README.md` documenting frontend setup and architecture
- [ ] 7.3 Create `frontend/package.json` skeleton (to be populated in frontend-config)

## 8. Root Level Configuration

- [ ] 8.1 Create/update `.gitignore` at project root covering backend and frontend patterns
- [ ] 8.2 Create/update root-level `README.md` documenting the monorepo structure and workflow
- [ ] 8.3 Create `.env.example` at project root (optional, for shared config)

## 9. Verification and Documentation

- [ ] 9.1 Verify all directories exist with correct hierarchy
- [ ] 9.2 Verify all `__init__.py` files exist in Python packages
- [ ] 9.3 Verify all placeholder files created
- [ ] 9.4 Test git can track the structure (no empty directories lost)
- [ ] 9.5 Create CONTRIBUTING.md documenting architectural rules and patterns
