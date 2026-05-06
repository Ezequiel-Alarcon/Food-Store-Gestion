# Food Store — E-Commerce Platform

> A full-stack e-commerce system for selling food products with Spec-Driven Development (SDD)

## 🎯 Overview

Food Store is a complete e-commerce solution featuring:
- **Frontend**: React + TypeScript + Vite with Feature-Sliced Design
- **Backend**: FastAPI + SQLModel + PostgreSQL with Clean Architecture
- **Payments**: MercadoPago integration
- **Authentication**: JWT + Role-Based Access Control (RBAC)
- **Admin**: Dashboard with metrics and management tools

## 📚 Documentation

Before developing, read these documents (in order):

| Document | Purpose |
|----------|---------|
| [`docs/Integrador.txt`](docs/Integrador.txt) | Technical specification (v5.0) — ERD, architecture, patterns |
| [`docs/Descripcion.txt`](docs/Descripcion.txt) | System overview — actors, stack, architecture |
| [`docs/Historias_de_usuario.txt`](docs/Historias_de_usuario.txt) | User stories (US-000 to US-076) with acceptance criteria |
| [`docs/CHANGES-ROADMAP.md`](docs/CHANGES-ROADMAP.md) | Change breakdown — 18 changes covering 77 user stories |

## 🏗️ Project Structure

```
food-store/
├── backend/                  # FastAPI backend (feature-first)
│   ├── app/
│   │   ├── core/             # Infrastructure patterns (UoW, Repository, Config)
│   │   └── modules/          # Domain modules (auth, products, orders, etc.)
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                 # React frontend (Feature-Sliced Design)
│   ├── src/
│   │   ├── app/              # Providers, routing
│   │   ├── pages/            # Route components
│   │   ├── features/         # User interactions (auth, cart, orders, admin)
│   │   ├── entities/         # Domain models, API clients
│   │   └── shared/           # UI components, utilities
│   ├── package.json
│   └── README.md
│
├── docs/                     # System documentation
│   ├── Integrador.txt        # Technical spec
│   ├── Descripcion.txt       # System overview
│   ├── Historias_de_usuario.txt  # User stories
│   └── CHANGES-ROADMAP.md    # Implementation roadmap
│
├── openspec/                 # SDD artifacts
│   ├── config.yaml           # Project context for AI
│   ├── specs/                # Archived specs (live documentation)
│   └── changes/              # Active change artifacts
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with API_URL and MercadoPago key

npm run dev
```

App: `http://localhost:5173`

## 📋 Development Workflow (SDD)

All work follows Spec-Driven Development with OPSX:

```
/opsx:explore   → Think through requirements
      ↓
/opsx:propose   → Create proposal + design + tasks
      ↓
/opsx:apply     → Implement tasks
      ↓
/opsx:archive   → Archive specs and close change
```

**Each change is a complete, tracked unit of work.**

### Current Changes

See [`docs/CHANGES-ROADMAP.md`](docs/CHANGES-ROADMAP.md) for the full roadmap.

| # | Change | Status | Epic |
|---|--------|--------|------|
| 1 | `infra-setup` | ✅ | EPIC 00 |
| 2 | `backend-config` | ⏳ | EPIC 00 |
| 3 | `frontend-config` | ⏳ | EPIC 00 |
| ... | ... | ... | ... |

## 🏛️ Architecture

### Backend: Clean Architecture with Feature-First Organization

```
Router → Service → UoW → Repository → Model
  ↓         ↓      ↓       ↓           ↓
HTTP    Logic   Trans    Data      Database
```

**Modules** (feature-first):
- `auth/` — Authentication, JWT, refresh tokens
- `usuarios/` — User management, RBAC
- `productos/` — Products, catalog, stock
- `pedidos/` — Orders, state machine, audit trail
- `pagos/` — MercadoPago integration
- `admin/` — Dashboard, metrics
- ...and more

### Frontend: Feature-Sliced Design (FSD)

```
app (providers)
 ↓
pages (routes)
 ↓
features (auth, cart, orders, admin)
 ↓
entities (models, API)
 ↓
shared (UI, utilities)
```

**Unidirectional imports**: Features never import from features or pages.

## 🔐 Authentication & Authorization

- **Registration & Login**: JWT tokens (access + refresh)
- **Roles**: CLIENT, GESTOR_STOCK, GESTOR_PEDIDOS, ADMIN
- **Rate Limiting**: 5 attempts per 15 minutes on login
- **Token Rotation**: Refresh tokens stored in DB

## 💳 Payments

- **Provider**: MercadoPago
- **Methods**: Credit/debit card, Rapipago, Pago Fácil
- **Webhooks**: IPN notifications for payment confirmation
- **PCI Compliance**: Card data tokenized client-side (SAQ-A)

## 📊 Database

- **Type**: PostgreSQL 15+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Migrations**: Alembic
- **Patterns**: Soft delete, snapshots, append-only audit trail

## 🎨 Styling

- **Framework**: Tailwind CSS 3.x
- **UI Components**: Custom + shadcn/ui (planned)
- **Approach**: Utility-first, no CSS files

## 🧪 Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm run test
```

## 📝 Commits

Follow conventional commits:

```
feat(module): add new feature
fix(module): fix bug
chore(module): maintenance
docs: update documentation
test(module): add tests
```

Example:
```bash
git commit -m "feat(auth): add refresh token rotation"
git commit -m "fix(orders): handle stock depletion race condition"
```

## 🤝 Contributing

1. **Read the docs** — Start with `docs/Integrador.txt`
2. **Understand the change** — Find it in `docs/CHANGES-ROADMAP.md`
3. **Create artifacts** — Proposal → Design → Tasks (using OPSX)
4. **Implement** — Follow the design and architecture patterns
5. **Review** — Specs are reviewed before coding
6. **Archive** — Specs go to `openspec/specs/` for reference

## 🛠️ Stack Highlights

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI | High performance, async, auto docs |
| Backend ORM | SQLModel | Type-safe queries, Pydantic validation |
| Database | PostgreSQL | Advanced types, CTEs, jsonb |
| Frontend | React 18 | Component-based, hooks, ecosystem |
| State | Zustand + TanStack Query | Simple, scalable, reactive |
| Styling | Tailwind | Utility-first, responsive, fast |
| Build | Vite | Lightning fast dev server and builds |

## 📞 Support

For questions or issues:
1. Check [`docs/`](docs/) for domain knowledge
2. Check `backend/README.md` or `frontend/README.md` for setup help
3. Review change artifacts in `openspec/changes/` for implementation context

## 📄 License

[Your license here]

---

**Last updated**: May 6, 2026  
**Spec Version**: 5.0  
**Stack Version**: 2024 Q4
