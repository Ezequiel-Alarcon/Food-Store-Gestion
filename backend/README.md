# Food Store Backend

## Overview

The Food Store backend is a FastAPI application that provides a REST API for the e-commerce system. It implements a **feature-first architecture** with **Clean Architecture layers** (Router → Service → UoW → Repository → Model).

## Directory Structure

```
backend/
├── app/
│   ├── core/                 # Cross-cutting infrastructure
│   │   ├── config.py         # App configuration
│   │   ├── database.py       # Database setup and session
│   │   ├── security.py       # JWT, bcrypt, auth utilities
│   │   ├── uow.py            # Unit of Work pattern
│   │   ├── repository.py     # BaseRepository[T] generic
│   │   ├── deps.py           # Dependency injection (get_current_user, etc.)
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── middleware.py     # Error handling, logging
│   │
│   ├── modules/              # Domain modules (feature-first)
│   │   ├── auth/             # Authentication & authorization
│   │   ├── usuarios/         # User management + RBAC
│   │   ├── direcciones/      # Delivery addresses
│   │   ├── categorias/       # Product categories
│   │   ├── ingredientes/     # Ingredients + allergens
│   │   ├── productos/        # Products + catalog
│   │   ├── pedidos/          # Orders + FSM
│   │   ├── pagos/            # MercadoPago integration
│   │   ├── admin/            # Admin dashboard + metrics
│   │   └── refreshtokens/    # Refresh token management
│   │
│   ├── main.py               # FastAPI app instantiation
│   └── __init__.py
│
├── db/
│   ├── migrations/           # Alembic migrations
│   ├── seed.py               # Initial data (roles, states, etc.)
│   └── __init__.py
│
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
│
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── main.py                   # Entry point for uvicorn
└── README.md
```

## Architecture: Layered with Dependency Flow

Each module follows this flow:

```
HTTP Request
    ↓
Router (validation, serialization)
    ↓
Service (business logic, orchestration)
    ↓
Unit of Work (transaction management)
    ↓
Repository (data access)
    ↓
Model (SQLModel entities)
    ↓
Database (PostgreSQL)
```

**Key rule**: Each layer only imports from layers below. Never upward.

## Module Template

Each module should follow this structure:

```
backend/app/modules/mymodule/
├── __init__.py              # Empty or expose main exports
├── model.py                 # SQLModel table definitions
├── schemas.py               # Pydantic request/response schemas
├── repository.py            # Data access layer
├── service.py               # Business logic
├── router.py                # FastAPI routes
└── [optional]
    ├── dependencies.py      # Module-specific dependencies
    └── constants.py         # Module constants
```

### Example: Creating a New Module

1. **Create directory** under `backend/app/modules/mymodule/`

2. **Define model** in `model.py`:
```python
from sqlmodel import SQLModel, Field

class MyEntity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

3. **Define schemas** in `schemas.py`:
```python
from pydantic import BaseModel

class MyEntityCreate(BaseModel):
    name: str

class MyEntityRead(BaseModel):
    id: int
    name: str
```

4. **Implement repository** in `repository.py`:
```python
from app.core.repository import BaseRepository
from .model import MyEntity

class MyEntityRepository(BaseRepository[MyEntity]):
    pass
```

5. **Implement service** in `service.py`:
```python
from app.core.uow import UnitOfWork
from .repository import MyEntityRepository

async def create_entity(uow: UnitOfWork, name: str):
    async with uow:
        entity = MyEntity(name=name)
        uow.my_entity.add(entity)
        await uow.commit()
    return entity
```

6. **Create router** in `router.py`:
```python
from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/v1/myentity", tags=["myentity"])

@router.post("/")
async def create(data: MyEntityCreate, current_user = Depends(get_current_user)):
    # Call service
    pass
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- pip and venv

### 1. Create virtual environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with actual values
```

### 4. Initialize database
```bash
alembic upgrade head
python -m app.db.seed
```

### 5. Run server
```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Key Patterns

### Unit of Work (UoW)
Manages database transactions and provides access to repositories:

```python
async with UnitOfWork() as uow:
    user = await uow.usuarios.get(id=1)
    user.email = "new@example.com"
    await uow.commit()
```

### BaseRepository[T]
Generic repository with common CRUD operations:

```python
repo = MyEntityRepository(session)
await repo.add(entity)
await repo.get(id=1)
await repo.update(id=1, data={...})
await repo.delete(id=1)
```

### Custom Exceptions
Use RFC 7807 problem detail format:

```python
from app.core.exceptions import ResourceNotFound

raise ResourceNotFound("User not found", resource_type="usuario", resource_id=123)
```

## Testing

Run tests with pytest:

```bash
pytest tests/
pytest tests/unit/  # Unit tests only
pytest tests/integration/  # Integration tests only
```

## Common Tasks

### Add a new endpoint
1. Create/modify `router.py` in the module
2. Add service function in `service.py`
3. Use `uow` to access repositories
4. Return response using schema from `schemas.py`

### Add validation
Extend Pydantic validators in `schemas.py`:

```python
from pydantic import field_validator

class MySchema(BaseModel):
    email: str
    
    @field_validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

### Handle errors
Use custom exceptions from `app.core.exceptions` and register exception handlers in `main.py`.

## Database Migrations

Create a migration after changing models:

```bash
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
```

## Rate Limiting

Applied to sensitive endpoints (e.g., login):

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
@app.post("/login")
@limiter.limit("5/15 minutes")
async def login(...):
    pass
```

## Contributing

- Follow PEP 8 (enforced with Black)
- Use type hints on all functions
- Add docstrings to public functions
- Write tests for new endpoints
- Run `black` before committing: `black backend/`

---

**For architectural questions, see the main README at the project root.**
