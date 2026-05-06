## ADDED Requirements

### Requirement: Backend module structure follows feature-first pattern
The backend SHALL organize code into feature modules, each containing its own router, service, repository, schemas, and model. Each module is located under `backend/app/modules/<module-name>/`.

#### Scenario: Module structure exists
- **WHEN** developer navigates to `backend/app/modules/`
- **THEN** the following directories exist: `auth/`, `usuarios/`, `direcciones/`, `categorias/`, `ingredientes/`, `productos/`, `pedidos/`, `pagos/`, `admin/`, `refreshtokens/`

#### Scenario: Core infrastructure is separate from modules
- **WHEN** developer looks for cross-cutting code
- **THEN** utilities like `BaseRepository`, `UnitOfWork`, config, database, and security are found in `backend/app/core/`

### Requirement: Frontend structure follows Feature-Sliced Design pattern
The frontend SHALL organize code into layers with unidirectional imports: app → pages → features → entities → shared. Each layer is located under `frontend/src/<layer>/`.

#### Scenario: FSD layers exist
- **WHEN** developer navigates to `frontend/src/`
- **THEN** the following directories exist: `app/`, `pages/`, `features/`, `entities/`, `shared/`

#### Scenario: Features are isolated
- **WHEN** developer examines `frontend/src/features/`
- **THEN** the following feature modules exist: `auth/`, `cart/`, `orders/`, `admin/`

### Requirement: Python package structure is valid
The backend SHALL have valid Python package markers (`__init__.py`) in all directories that define modules or packages.

#### Scenario: Core package is valid
- **WHEN** backend code imports from `backend.app.core`
- **THEN** the import succeeds because `__init__.py` exists in `backend/app/` and `backend/app/core/`

#### Scenario: Module packages are valid
- **WHEN** backend code imports from `backend.app.modules.auth`
- **THEN** the import succeeds because `__init__.py` exists in all intermediate directories
