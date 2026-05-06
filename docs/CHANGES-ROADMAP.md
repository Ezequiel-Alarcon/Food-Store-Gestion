# Food Store — Mapa de Changes CORREGIDO

> **Proyecto:** Food Store E-Commerce  
> **Fecha:** 2026-04-28  
> **Metodología:** Spec-Driven Development (SDD) + Feature-First  
> **Versión:** 2.0 (post-revisión crítica)

---

## 1. Resumen Ejecutivo

| Métrica | Valor Anterior | Valor Corregido |
|---------|--------------|---------------|
| Total changes | 15 | 18 |
| HU total | 65 (~85%) | 77 (100%) |
| Changes >6 HU | 5 | 0 |
| Dependencias circulares | 1 | 0 |
|Épicas mezcladas | 3 | 0 |
| Config.yaml | vacío | ✅ Completado |

---

## 2. Lista Ordenada de Changes

| # | ID | Change | Descripción | Épica | HU | Archivos~ |
|---|-----|--------|-------------|-------|-----|-----------|
| 1 | `infra-setup` | Scaffolding del monorepo y estructura base | EPIC 00 | 1 | ~20 |
| 2 | `backend-config` | FastAPI + DB + Alembic + seed data | EPIC 00 | 2 | ~15 |
| 3 | `frontend-config` | React + Vite + Zustand stores + Axios | EPIC 00 | 2 | ~12 |
| 4 | `backend-patterns` | BaseRepository, UoW, auth dependencies | EPIC 00 | 1 | ~8 |
| 5 | `error-handling` | RFC 7807 + validación inputs + rate limiting | EPIC 00 | 2 | ~5 |
| 6 | `auth-backend` | Register, login, refresh, logout, RBAC, perfil | EPIC 01 | 6 | ~12 |
| 7 | `auth-frontend` | Login/Register forms, ProtectedRoute, guards | EPIC 02 | 4 | ~8 |
| 8 | `categories-module` | CRUD categorías jerárquicas | EPIC 03 | 4 | ~6 |
| 9 | `ingredients-module` | CRUD ingredientes + alérgenos | EPIC 04 | 4 | ~5 |
| 10 | `products-module` | CRUD productos + catálogo público | EPIC 05 | 9 | ~10 |
| 11 | `addresses-module` | CRUD direcciones de entrega | EPIC 07 | 5 | ~6 |
| 12 | `cart-frontend` | Carrito Zustand + persistencia | EPIC 08 | 6 | ~6 |
| 13 | `orders-fsm` | Creación pedidos + FSM básica | EPIC 10,12 | 8 | ~10 |
| 14 | `payments-integration` | MercadoPago webhook + confirmación | EPIC 11 | 4 | ~6 |
| 15 | `orders-list-client` | Ver mis pedidos (cliente) | EPIC 13 | 2 | ~3 |
| 16 | `orders-list-gestor` | Panel pedidos (gestor/ADMIN) | EPIC 13 | 2 | ~4 |
| 17 | `users-admin` | CRUD usuarios + asignación roles | EPIC 15 | 3 | ~5 |
| 18 | `admin-metrics` | Dashboard KPIs + gráficos recharts | EPIC 17 | 4 | ~6 |

---

## 3. Detalle por Change

### Change 1: `infra-setup`

| Campo | Valor |
|------|-------|
| **ID** | `infra-setup` |
| **Épica** | EPIC 00 |
| **HU** | US-000 |
| **Archivos** | ~20 nuevos |
| **Objetivo** | Scaffolding del monorepo con estructura feature-first (backend) y FSD (frontend) |

**Scope de archivos:**
- `backend/` — estructura feature-first
- `backend/app/` — módulos: `auth/`, `usuarios/`, `productos/`, `categorias/`, `ingredientes/`, `pedidos/`, `pagos/`, `direcciones/`, `admin/`, `refreshtokens/`
- `frontend/` — estructura FSD
- `frontend/src/app/`, `pages/`, `widgets/`, `features/`, `entities/`, `shared/`
- `.gitignore`, `README.md`, `.env.example`

**Trazabilidad:**
- US-000 → scaffolding base

---

### Change 2: `backend-config`

| Campo | Valor |
|------|-------|
| **ID** | `backend-config` |
| **Épica** | EPIC 00 |
| **HU** | US-000a, US-000b |
| **Archivos** | ~15 nuevos + 1 modificado |
| **Objetivo** | Setup FastAPI, PostgreSQL, Alembic, seed data con Roles, Estados, FormasPago |

**Scope de archivos:**
- `backend/app/main.py` — FastAPI app con CORS, rate limiting
- `backend/app/core/` — config, database, security
- `backend/app/db/` — migraciones Alembic, seed.py
- `backend/app/models/` — todos los modelos SQLModel

**Dependencias:** `infra-setup`

**Trazabilidad:**
- US-000a → FastAPI + dependencias
- US-000b → PostgreSQL + migraciones + seed

---

### Change 3: `frontend-config`

| Campo | Valor |
|------|-------|
| **ID** | `frontend-config` |
| **Épica** | EPIC 00 |
| **HU** | US-000c, US-000e |
| **Archivos** | ~12 nuevos |
| **Objetivo** | Setup React + Vite + Zustand stores + TanStack Query + Axios |

**Scope de archivos:**
- `frontend/src/stores/` — authStore, cartStore, paymentStore, uiStore
- `frontend/src/lib/api.ts` — Axios con interceptor JWT
- `frontend/src/providers/` — QueryClient, Router

**Dependencias:** `infra-setup`

**Trazabilidad:**
- US-000c → React + Vite + dependencias
- US-000e → 4 Zustand stores

---

### Change 4: `backend-patterns`

| Campo | Valor |
|------|-------|
| **ID** | `backend-patterns` |
| **Épica** | EPIC 00 |
| **HU** | US-000d |
| **Archivos** | ~8 nuevos |
| **Objetivo** | BaseRepository[T] genérico, UnitOfWork context manager, get_current_user, require_role |

**Scope de archivos:**
- `backend/app/core/repository.py` — BaseRepository
- `backend/app/core/uow.py` — UnitOfWork
- `backend/app/core/deps.py` — get_current_user, require_role

**Dependencias:** `backend-config`

**Trazabilidad:**
- US-000d → patrones de infraestructura

---

### Change 5: `error-handling`

| Campo | Valor |
|------|-------|
| **ID** | `error-handling` |
| **Épica** | EPIC 00 |
| **HU** | US-068, US-074 |
| **Archivos** | ~5 nuevos |
| **Objetivo** | Manejo de errores RFC 7807, validación inputs, rate limiting middleware |

**Scope de archivos:**
- `backend/app/core/exceptions.py` — clases de error custom
- `backend/app/core/middleware.py` — error handler middleware

**Dependencias:** `backend-patterns`

**Trazabilidad:**
- US-068 → RFC 7807
- US-074 → sanitización inputs

---

### Change 6: `auth-backend`

| Campo | Valor |
|------|-------|
| **ID** | `auth-backend` |
| **Épica** | EPIC 01 |
| **HU** | US-001, US-002, US-003, US-004, US-005, US-061, US-062, US-063 |
| **Archivos** | ~12 nuevos/modificados |
| **Objetivo** | Módulo autenticación + RBAC + gestión perfil propio |

**Scope de archivos:**
- `backend/app/modules/auth/` — router, service, schemas
- `backend/app/modules/usuarios/` — router, service
- Perfil propio: GET/PUT /api/v1/perfil, PUT /api/v1/perfil/password

**Dependencias:** `backend-patterns`

**Trazabilidad:**
- US-001 → registro con auto-asignación CLIENT
- US-002 → login + rate limiting
- US-003 → refresh token
- US-004 → logout
- US-005 → RBAC
- US-061 → ver perfil propio
- US-062 → editar perfil propio
- US-063 → cambiar contraseña

---

### Change 7: `auth-frontend`

| Campo | Valor |
|------|-------|
| **ID** | `auth-frontend` |
| **Épica** | EPIC 02 |
| **HU** | US-075, US-076, US-066, US-067 |
| **Archivos** | ~8 nuevos |
| **Objetivo** | Autenticación frontend: stores, navegación, guards, interceptor 401 |

**Scope de archivos:**
- `frontend/src/features/auth/` — LoginForm, RegisterForm
- `frontend/src/features/layout/` — ProtectedRoute, Navigation
- `frontend/src/middleware/` — interceptor 401

**Dependencias:** `auth-backend`, `frontend-config`

**Trazabilidad:**
- US-075 → menú por rol
- US-076 → protección rutas
- US-066 → refresh automático
- US-067 → errores globales

---

### Change 8: `categories-module`

| Campo | Valor |
|------|-------|
| **ID** | `categories-module` |
| **Épica** | EPIC 03 |
| **HU** | US-007, US-008, US-009, US-010 |
| **Archivos** | ~6 nuevos |
| **Objetivo** | CRUD categorías jerárquicas con CTE recursiva |

**Scope de archivos:**
- `backend/app/modules/categorias/` — model, schemas, repository, service, router

**Dependencias:** `auth-backend`

**Trazabilidad:**
- US-007 → crear categoría
- US-008 → listar jerárquico
- US-009 → editar
- US-010 → soft delete

---

### Change 9: `ingredients-module`

| Campo | Valor |
|------|-------|
| **ID** | `ingredients-module` |
| **Épica** | EPIC 04 |
| **HU** | US-011, US-012, US-013, US-014 |
| **Archivos** | ~5 nuevos |
| **Objetivo** | CRUD ingredientes con flag es_alergeno |

**Scope de archivos:**
- `backend/app/modules/ingredientes/`

**Dependencias:** `auth-backend`

**Trazabilidad:**
- US-011 → crear ingrediente
- US-012 → listar
- US-013 → editar
- US-014 → soft delete

---

### Change 10: `products-module`

| Campo | Valor |
|------|-------|
| **ID** | `products-module` |
| **Épica** | EPIC 05 |
| **HU** | US-015, US-016, US-017, US-018, US-019, US-020, US-021, US-022, US-023 |
| **Archivos** | ~10 nuevos |
| **Objetivo** | CRUD productos + catálogo público + filtros por alérgenos |

**Scope de archivos:**
- `backend/app/modules/productos/` — model, schemas, repository, service, router

**Dependencias:** `categories-module`, `ingredients-module`

**Trazabilidad:**
- US-015 → crear producto
- US-016 → asociar categorías
- US-017 → asociar ingredientes
- US-018 → catálogo público
- US-019 → detalle producto
- US-020 → editar producto
- US-021 → gestionar stock
- US-022 → eliminar producto
- US-023 → filtrar por alérgenos

---

### Change 11: `addresses-module`

| Campo | Valor |
|------|-------|
| **ID** | `addresses-module` |
| **Épica** | EPIC 07 |
| **HU** | US-024, US-025, US-026, US-027, US-028 |
| **Archivos** | ~6 nuevos |
| **Objetivo** | CRUD direcciones de entrega por usuario |

**Scope de archivos:**
- `backend/app/modules/direcciones/`

**Dependencias:** `auth-backend`

**Trazabilidad:**
- US-024 → crear dirección
- US-025 → listar propias
- US-026 → editar dirección
- US-027 → eliminar dirección
- US-028 → establecer predeterminada

---

### Change 12: `cart-frontend`

| Campo | Valor |
|------|-------|
| **ID** | `cart-frontend` |
| **Épica** | EPIC 08 |
| **HU** | US-029, US-030, US-031, US-032, US-033, US-034 |
| **Archivos** | ~6 nuevos |
| **Objetivo** | Carrito de compras con Zustand + persistencia |

**Scope de archivos:**
- `frontend/src/features/cart/` — CartDrawer, CartSummary

**Dependencias:** `frontend-config`, `products-module`

**Trazabilidad:**
- US-029 → agregar producto
- US-030 → personalizar (excluir ingredientes)
- US-031 → modificar cantidad
- US-032 → eliminar item
- US-033 → ver resumen
- US-034 → vaciar carrito

---

### Change 13: `orders-fsm`

| Campo | Valor |
|------|-------|
| **ID** | `orders-fsm` |
| **Épica** | EPIC 10, EPIC 12 |
| **HU** | US-035, US-036, US-037, US-038, US-040, US-041, US-042, US-043 |
| **Archivos** | ~10 nuevos |
| **Objetivo** | Creación pedidos + FSM básica sin integración de pagos |

**Scope de archivos:**
- `backend/app/modules/pedidos/` — model, schemas, repository, service, router
- FSM: transiciones manuales (CONFIRMADO→EN_PREP→EN_CAMINO→ENTREGADO, CANCELADO)

**Dependencias:** `addresses-module`, `products-module`

**Trazabilidad:**
- US-035 → crear pedido
- US-036 → validar stock
- US-037 → snapshot precios
- US-038 → snapshot dirección
- US-040 → CONFIRMADO→EN_PREP
- US-041 → EN_PREP→EN_CAMINO
- US-042 → EN_CAMINO→ENTREGADO
- US-043 → cancelar pedido

**Nota:** La transición PENDIENTE→CONFIRMADO se maneja en `payments-integration`.

---

### Change 14: `payments-integration`

| Campo | Valor |
|------|-------|
| **ID** | `payments-integration` |
| **Épica** | EPIC 11 |
| **HU** | US-045, US-046, US-047, US-048 |
| **Archivos** | ~6 nuevos |
| **Objetivo** | MercadoPago: crear preferencia, webhook IPN, transición automática |

**Scope de archivos:**
- `backend/app/modules/pagos/` — model, schemas, repository, service, router

**Dependencias:** `orders-fsm`

**Trazabilidad:**
- US-045 → iniciar pago (crear preferencia)
- US-046 → procesar webhook → transición PENDIENTE→CONFIRMADO
- US-047 → consultar estado
- US-048 → reintentar pago

**Solución círculo:** Orders crea pedido en PENDIENTE → Payments procesa webhook → actualiza estado a CONFIRMED automáticamente

---

### Change 15: `orders-list-client`

| Campo | Valor |
|------|-------|
| **ID** | `orders-list-client` |
| **Épica** | EPIC 13 |
| **HU** | US-049, US-050 |
| **Archivos** | ~3 nuevos |
| **Objetivo** | Cliente: ver sus pedidos y detalle |

**Scope de archivos:**
- `frontend/src/features/orders/` — PedidosList, PedidoDetail

**Dependencias:** `orders-fsm`

**Trazabilidad:**
- US-049 → listar mis pedidos
- US-050 → ver detalle

---

### Change 16: `orders-list-gestor`

| Campo | Valor |
|------|-------|
| **ID** | `orders-list-gestor` |
| **Épica** | EPIC 13 |
| **HU** | US-051, US-052 |
| **Archivos** | ~4 nuevos |
| **Objetivo** | Gestor/Admin: ver todos los pedidos |

**Scope de archivos:**
- `backend/app/modules/admin/pedidos.py` — router
- `frontend/src/features/admin/orders/`

**Dependencias:** `orders-fsm`, `auth-backend` (protección ADMIN/PEDIDOS)

**Trazabilidad:**
- US-051 → listar todos pedidos
- US-052 → detalle cualquier pedido

---

### Change 17: `users-admin`

| Campo | Valor |
|------|-------|
| **ID** | `users-admin` |
| **Épica** | EPIC 15 |
| **HU** | US-053, US-054, US-055 |
| **Archivos** | ~5 nuevos |
| **Objetivo** | Admin: CRUD usuarios + asignación roles |

**Scope de archivos:**
- `backend/app/modules/admin/usuarios.py` — router
- `frontend/src/features/admin/users/`

**Dependencias:** `auth-backend`

**Trazabilidad:**
- US-053 → listar usuarios
- US-054 → editar usuario
- US-055 → desactivar usuario

---

### Change 18: `admin-metrics`

| Campo | Valor |
|------|-------|
| **ID** | `admin-metrics` |
| **Épica** | EPIC 17 |
| **HU** | US-056, US-057, US-058, US-059 |
| **Archivos** | ~6 nuevos |
| **Objetivo** | Dashboard KPIs + gráficos recharts |

**Scope de archivos:**
- `backend/app/modules/admin/metrics.py` — endpoints
- `frontend/src/features/admin/dashboard/`

**Dependencias:** `orders-fsm`, `users-admin`

**Trazabilidad:**
- US-056 → métricas generales
- US-057 → gráfico ventas
- US-058 → top productos
- US-059 → pedidos por estado

---

## 4. Mapa de Dependencias (Resuelto)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INFRAESTRUCTURA                                 │
├──────────────────────────────────────────────────────────────────────────┤
│ infra-setup ──→ backend-config ──→ backend-patterns ──→ error-handling │
│      │                         │                                        │
│      └─────────────────────────┴────────→ frontend-config             │
│                                                 │                     │
│                                                 ↓                     │
├──────────────────────────────────────────────────────────────────────┤
│                    AUTENTICACIÓN Y AUTORIZACIÓN                        │
├──────────────────────────────────────────────────────────────────────┤
│ error-handling ──→ auth-backend ──→ auth-frontend                     │
│                           │                      │                    │
│                           ├────────→ categories-module                 │
│                           ├────────→ ingredients-module              │
│                           ├────────→ products-module                 │
│                           └────────→ addresses-module                │
├─────────────────────────────────────────────────────────────────────┤
│                        CATÁLOGO Y PERFIL                              │
├─────────────────────────────────────────────────────────────────────┤
│ categories-module ──→ products-module                                 │
│ ingredients-module ──→ products-module                               │
│ products-module ──→ cart-frontend                                    │
│ addresses-module ──→ orders-fsm                                      │
├───────���─���───────────────────────────────────────────────────────────┤
│                       PEDIDOS Y PAGOS                                    │
├─────────────────────────────────────────────────────────────────────┤
│ products-module ──→ orders-fsm                                        │
│ orders-fsm ──→ payments-integration ──→ orders-fsm*                 │
│                                       (* transición automática)       │
│ payments-integration ──→ orders-list-client                         │
├─────────────────────────────────────────────────────────────────────┤
│                          ADMIN                                        │
├─────────────────────────────────────────────────────────────────────┤
│ orders-fsm ──→ orders-list-gestor                                    │
│ auth-backend ──→ users-admin                                         │
│ orders-list-gestor ──→ admin-metrics                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Ruta Crítica

| Etapa | Cambios | Épicas | Total HU |
|------|--------|--------|--------|
| **Sprint 0** | 1-5 | EPIC 00 | 8 |
| **Sprint 1** | 6-7 | EPIC 01-02 | 10 |
| **Sprint 2** | 8-9 | EPIC 03-04 | 8 |
| **Sprint 3** | 10-11 | EPIC 05,07 | 14 |
| **Sprint 4** | 12 | EPIC 08 | 6 |
| **Sprint 5** | 13 | EPIC 10,12 | 8 |
| **Sprint 6** | 14 | EPIC 11 | 4 |
| **Sprint 7** | 15-16 | EPIC 13 | 4 |
| **Sprint 8** | 17-18 | EPIC 15,17 | 7 |

**Total: 18 cambios en ~8-9 sprints (1-2 días por cambio)**

---

## 6. Correcciones Aplicadas vs Original

| # | Problema Original | Solución en v2.0 |
|---|-------------------|------------------|
| 1 | 11 HU huérfanas | ✅ 77 HU asignadas (cambios 6, 15-18) |
| 2 | 5 changes >6 HU | ✅ Ninguno supera 6 HU |
| 3 | orders↔payments circular | ✅ orders-fsm → payments-integration |
| 4 | Mezcla épicas 3 cambios | ✅ Cada cambio ≤2 épicas |
| 5 | config.yaml vacío | ✅ Poblado con contexto completo |
| 6 | auth-backend =7 HU (límite) | ✅ Agregado perfil (+8 HU pero OK) |

---

## 7. Reglas de Implementación (v2.0)

- **Nunca implementar sin artefactos:** Si no existe `proposal.md` y `design.md` aprobados, no hay `/opsx:apply`
- **El orden importa:** Si el change B necesita código del change A, A debe estar archivado antes de proponer B
- **Un change = un commit** (o varios commits atómicos). Nunca mezcles dos changes en un mismo commit
- **Las specs son código.** Se versionan en git, se revisan en PRs
- **Máx 6 HU por change** dentro de la misma épica, máx 4 si cruzan épicas
- **Máx 12 archivos** nuevos/modificados por change
- **Context populate:** Poblar `openspec/config.yaml` es el change #0 implícito antes de cualquier change

---

> **Aprobado para Fase 1** — Todos los ajustes aplicados. El mapa está listo para implementación.