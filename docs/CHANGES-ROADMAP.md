# Food Store — Mapa de Changes

> **Proyecto:** Food Store E-Commerce  
> **Fecha:** 2026-04-13  
> **Metodología:** Spec-Driven Development (SDD) + Feature-First

---

## 1. Lista Ordenada de Changes

| # | ID | Change | Descripción | Épica |
|---|-----|--------|-------------|-------|
| 1 | `infra-setup` | Setup del repositorio y estructura base | EPIC 00 |
| 2 | `backend-config` | Configuración del backend (FastAPI + DB + seed) | EPIC 00 |
| 3 | `frontend-config` | Configuración del frontend (React + Vite + stores) | EPIC 00 |
| 4 | `backend-patterns` | Patrones de infraestructura (BaseRepository, UoW, auth deps) | EPIC 00 |
| 5 | `error-handling` | Manejo de errores estandarizado + validación inputs | EPIC 00 |
| 6 | `auth-backend` | Módulo de autenticación (register, login, refresh, logout, RBAC) | EPIC 01 |
| 7 | `auth-frontend` | Autenticación en frontend (stores, navegación, guards) | EPIC 01-02 |
| 8 | `categories-module` | CRUD de categorías jerárquicas | EPIC 03 |
| 9 | `ingredients-module` | CRUD de ingredientes y alérgenos | EPIC 04 |
| 10 | `products-module` | CRUD completo de productos + catálogo público | EPIC 05 |
| 11 | `addresses-module` | CRUD de direcciones de entrega | EPIC 06 |
| 12 | `cart-frontend` | Carrito de compras con Zustand | EPIC 07 |
| 13 | `orders-backend` | Creación y gestión de pedidos + FSM | EPIC 08-09 |
| 14 | `payments-module` | Integración con MercadoPago (webhook + checkout) | EPIC 10 |
| 15 | `admin-panel` | Panel de administración + dashboard + métricas | EPIC 11-12 |

---

## 2. Detalle por Change

### Change 1: `infra-setup`

**Funcionalidad:** Scaffolding del monorepo con estructura feature-first (backend) y FSD (frontend).

- **User Stories:** US-000
- **Archivos a crear:**
  - `/backend` con módulos: `auth/`, `usuarios/`, `productos/`, `categorias/`, `ingredientes/`, `pedidos/`, `pagos/`, `direcciones/`, `admin/`, `refreshtokens/`
  - `/frontend` con estructura FSD: `app/`, `pages/`, `widgets/`, `features/`, `entities/`, `shared/`
  - `.gitignore`, `README.md`, `.env.example` (ambos proyectos)
- **Dependencias:** Ninguna (punto de partida)

---

### Change 2: `backend-config`

**Funcionalidad:** Setup del backend con FastAPI, SQLModel, Alembic, PostgreSQL y seed data.

- **User Stories:** US-000a, US-000b
- **Criterios técnicos:**
  - FastAPI con CORS, rate limiting middleware
  - PostgreSQL con todas las tablas del ERD v5
  - Migraciones Alembic reversibles
  - Seed: 4 Roles, 6 EstadoPedido, 2 FormaPago, usuario admin
- **Dependencias:**
  - `infra-setup` — requiere la estructura existente

---

### Change 3: `frontend-config`

**Funcionalidad:** Setup del frontend con React, TypeScript, Vite, Tailwind y stores Zustand.

- **User Stories:** US-000c, US-000e
- **Archivos críticos:**
  - 4 Zustand stores: `authStore`, `cartStore`, `paymentStore`, `uiStore`
  - Axios con interceptor JWT y refresh automático
  - TanStack Query configurado
- **Dependencias:**
  - `infra-setup` — requiere estructura frontend existente

---

### Change 4: `backend-patterns`

**Funcionalidad:** Implementación de patrones de infraestructura reutilizables.

- **User Stories:** US-000d
- **Patrones a implementar:**
  - `BaseRepository[T]` genérico con soft-delete
  - `UnitOfWork` como context manager (commit/rollback automático)
  - `get_current_user` dependency
  - `require_role(roles[])` dependency factory
- **Dependencias:**
  - `backend-config` — requiere DB y modelos

---

### Change 5: `error-handling`

**Funcionalidad:** Manejo de errores estandarizado (RFC 7807) y validación de inputs.

- **User Stories:** US-068, US-074
- **Criterios:**
  - Exception handlers custom (ValidationError, UnauthorizedError, etc.)
  - Middleware global de formateo de errores
  - Validation pipes para XSS y SQL injection
- **Dependencias:**
  - `backend-patterns` — requiere UoW y dependencies

---

### Change 6: `auth-backend`

**Funcionalidad:** Módulo completo de autenticación y autorización JWT.

- **User Stories:** US-001, US-002, US-003, US-004, US-005, US-006, US-073
- **Endpoints:**
  - `POST /auth/register` — registro con auto-asignación rol CLIENT
  - `POST /auth/login` — JWT + rate limiting (5 intentos/15min)
  - `POST /auth/refresh` — rotación de tokens
  - `POST /auth/logout` — invalidación de refresh token
  - `PUT /admin/users/:id/role` — asignación RBAC
- **Dependencias:**
  - `backend-patterns` — requiere UoW y get_current_user

---

### Change 7: `auth-frontend`

**Funcionalidad:** Autenticación en frontend: stores, navegación y guards.

- **User Stories:** US-075, US-076, US-066, US-067
- **Componentes:**
  - LoginForm, RegisterForm
  - ProtectedRoute HOC
  - Navigation adaptativa por rol
  - Interceptor de 401 con refresh automático
  - Manejo global de errores HTTP
- **Dependencias:**
  - `auth-backend` — requiere endpoints operativos
  - `frontend-config` — requiere stores base

---

### Change 8: `categories-module`

**Funcionalidad:** CRUD completo de categorías con jerarquía recursiva.

- **User Stories:** US-007, US-008, US-009, US-010
- **Endpoints:**
  - `POST /categorias` — crear (con validación de ciclos)
  - `GET /categorias` — listado público con árbol anidado (CTE recursivo)
  - `PUT /categorias/:id` — editar
  - `DELETE /categorias/:id` — soft delete con validación de productos
- **Dependencias:**
  - `auth-backend` — requiere protección por rol (STOCK)

---

### Change 9: `ingredients-module`

**Funcionalidad:** CRUD de ingredientes con flag de alérgenos.

- **User Stories:** US-011, US-012, US-013, US-014
- **Endpoints:**
  - `POST /ingredientes`
  - `GET /ingredientes` — filtrable por `es_alergeno`
  - `PUT /ingredientes/:id`
  - `DELETE /ingredientes/:id` — soft delete
- **Dependencias:**
  - `auth-backend` — requiere protección por rol (STOCK)

---

### Change 10: `products-module`

**Funcionalidad:** CRUD completo de productos + catálogo público + filtrado por alérgenos.

- **User Stories:** US-015, US-016, US-017, US-018, US-019, US-020, US-021, US-022, US-023
- **Módulos:**
  - Productos: CRUD + gestión de stock
  - Producto-Categoria (M2M)
  - Producto-Ingrediente (M2M con `es_removible`)
  - Catálogo público con paginación, filtros, búsqueda
  - Filtrado por alérgenos
- **Dependencias:**
  - `categories-module` — requiere categorías existentes
  - `ingredients-module` — requiere ingredientes existentes

---

### Change 11: `addresses-module`

**Funcionalidad:** CRUD de direcciones de entrega por usuario.

- **User Stories:** US-024, US-025, US-026, US-027, US-028
- **Endpoints:**
  - `POST /direcciones`
  - `GET /direcciones` — solo propias
  - `PUT /direcciones/:id`
  - `DELETE /direcciones/:id`
  - `PATCH /direcciones/:id/principal` — única dirección principal
- **Dependencias:**
  - `auth-backend` — requiere autenticación

---

### Change 12: `cart-frontend`

**Funcionalidad:** Carrito de compras con Zustand y persistencia.

- **User Stories:** US-029, US-030, US-031, US-032, US-033, US-034
- **Funcionalidades:**
  - Agregar/quitar productos
  - Personalización (exclusión de ingredientes)
  - Persistencia en localStorage (sobrevive a refresh/logout)
  - Cálculo de totales
- **Dependencias:**
  - `frontend-config` — requiere cartStore
  - `products-module` — requiere catálogo operativo

---

### Change 13: `orders-backend`

**Funcionalidad:** Creación de pedidos + FSM (máquina de 6 estados) + audit trail.

- **User Stories:** US-035, US-036, US-037, US-038, US-039, US-040, US-041, US-042, US-043, US-044, US-045, US-046, US-047, US-048
- **Características:**
  - Creación atómica con UoW (snapshots de precio/dirección)
  - Validación de stock (SELECT FOR UPDATE)
  - Decremento automático de stock al confirmar
  - Restauración de stock al cancelar
  - HistorialEstadoPedido append-only
  - Transiciones validadas por FSM
- **Dependencias:**
  - `addresses-module` — requiere direcciones
  - `products-module` — requiere stock
  - `payments-module` — requiere integración con MercadoPago

---

### Change 14: `payments-module`

**Funcionalidad:** Integración con MercadoPago Checkout API + webhook IPN.

- **User Stories:** US-045, US-046, US-047, US-048
- **Endpoints:**
  - `POST /pagos/crear-preferencia` — crea preferencia de pago
  - `POST /pagos/webhook` — Procesa IPN de MercadoPago
  - `GET /pagos/pedido/:id` — consulta pagos de un pedido
- **Características:**
  - Idempotency key para evitar cobros duplicados
  - Transición automática PENDIENTE → CONFIRMADO
  - Restauración de stock al rechazar
- **Dependencias:**
  - `orders-backend` — requiere FSM operativa

---

### Change 15: `admin-panel`

**Funcionalidad:** Panel de administración completo con dashboard y métricas.

- **User Stories:** US-049, US-050, US-051, US-052, US-053, US-054, US-055, US-056, US-057, US-058, US-059, US-060
- **Módulos:**
  - Dashboard con KPIs y gráficos (recharts)
  - Gestión de usuarios (CRUD + asignación de roles)
  - Gestión de pedidos (avance de estados para PEDIDOS/ADMIN)
  - Gestión de stock
  - Métricas del negocio
- **Dependencias:**
  - `orders-backend` — requiere pedidos
  - `products-module` — requiere gestión de stock

---

## 3. Mapa de Dependencias

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INFRAESTRUCTURA                       │
├──────────────────────────────────────────────────────────────────────┤
│ infra-setup ──→ backend-config ──→ backend-patterns ──→ error-handling │
│      │                   │                                       │
│      └───────────────────┴────────→ frontend-config               │
│                                    │                             │
│                                    ↓                             │
├──────────────────────────────────────────────────────────────────────���
│                 AUTENTICACIÓN Y AUTORIZACIÓN                 │
├──────────────────────────────────────────────────────────────────────┤
│ backend-patterns ──→ auth-backend ──→ auth-frontend         │
│                           │                                  │
│                           └────────→ categories-module       │
│                           └────────→ ingredients-module     │
│                           └────────→ products-module         │
│                           └────────→ addresses-module       │
├──────────────────────────────────────────────────────────────┤
│                    CATÁLOGO Y PERFIL                       │
├──────────────────────────────────────────────────────────────────────┤
│ categories-module ──→ products-module                     │
│ ingredients-module ──→ products-module                     │
│ products-module ──→ cart-frontend                           │
│ auth-frontend ──→ addresses-module                        │
│ auth-frontend ──→ products-module                       │
├──────────────────────────────────────────────────────────────┤
│                      PEDIDOS Y PAGOS                         │
├──────────────────────────────────────────────────────────────────────┤
│ addresses-module ──→ orders-backend                        │
│ products-module ──→ orders-backend                         │
│ orders-backend ──→ payments-module ──→ orders-backend*    │
│                                            (* ciclo: pago confirmado → decrementa stock)                                           │
├──────────────────────────────────────────────────────────────────────┤
│                       ADMIN                                │
├──────────────────────────────────────────────────────────────────────┤
│ orders-backend ──→ admin-panel                            │
│ products-module ──→ admin-panel                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Análisis Crítico del Orden Propuesto

### Aspectos Positivos

1. **Infraestructura primero:** No se puede implementar nada sin DB, modelos y patrones. Las US-000x son el foundations del sistema.

2. **Auth temprana:** La autenticación es requisito para casi todo. Implementarla en el change 6 desbloquea múltiples cambios posteriores.

3. **Separación por módulos funcionales:** Cada change es autocontenido y entregable. Un change = un incremento funcional coherente.

4. **Catálogo antes que pedidos:** Los productos deben existir antes de poder comprarlos. Las dependencias respetan esta lógica de negocio.

5. **FSM después del catálogo:** La máquina de estados requiere productos, direcciones y stock. El change 13 depende del 10 y 11.

### Puntos de Atención

1. **Change 13 y 14 tienen dependencia circular parcial:**
   - `orders-backend` necesita `payments-module` para la transición automática PENDIENTE→CONFIRMADO
   - `payments-module` necesita `orders-backend` para crear el pedido
   
   **Solución propuesta:** Crear el change `orders-backend` primero con la FSM básica, luego `payments-module` extiende la transición automática.

2. **Frontend tiene menos cambios que el backend:**
   - El change 7 agrupa autenticación + navegación + errores
   - El change 12 agrupa el carrito completo
   - Esto reduce el overhead de cambios pequeños

3. **No hay change separado para "perfil del cliente":**
   - US-061, US-062 están en el change 6 (auth-backend) para datos del usuario
   - El change 11 cubre las direcciones

### Alternativas Consideradas

| Alternativa | Cambios | Pros | Contras |
|-------------|---------|------|---------|
| Separar perfil en change propio | +1 change | Más granular | Overhead de coordinación |
| Un change por épica | 13 changes |Simple | Changes muy grandes, difícil de completar |
| Cambios por capa (backend/frontend) | 2 changes |Muy simple | Sin coherencia funcional |

La propuesta actual balancea granularidad con coherencia funcional: cada change es un módulo funcional completo (sus modelos, APIs, frontend si corresponde).

---

## 5. Ruta Crítica

| Métrica | Valor |
|--------|-------|
| **Total de changes** | 15 |
| **Épicas cubiertas** | 13 |
| **User Stories integradas** | ~70 |

**Ruta crítica:** `infra-setup` → `backend-config` → `frontend-config` → `backend-patterns` → `auth-backend` → `auth-frontend` → `products-module` → `cart-frontend` → `orders-backend` → `payments-module` → `admin-panel`

**Estimación:** ~15 sprints de desarrollo (1-2 días por change) o 5-7 semanas (sprints de 2 semanas con 3-4 cambios por sprint).

---

## 6. Reglas de Implementación

- **Nunca implementar sin artefactos.** Si no existe `proposal.md` y `design.md` aprobados, no hay `/opsx:apply`.
- **El orden importa.** Si el change B necesita código del change A, A tiene que estar archivado antes de proponer B.
- **Un change = un commit** (o varios commits atómicos). Nunca mezcles dos changes en un mismo commit.
- **Las specs son código.** Se versionan en git, se revisan en PRs, evolucionan con el proyecto.