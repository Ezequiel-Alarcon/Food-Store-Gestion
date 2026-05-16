# Food Store — Asignación por Team (Pipeline Backend-First)

> **Proyecto:** Food Store E-Commerce
> **Fecha:** 2026-05-14
> **Distribución:** 43 changes entre 5 integrantes
> **Método:** Secuencial con fases Backend → Frontend → Deuda Técnica
> **Versión:** 3.0 (sync 33 changes + Fase 4 pendientes)

---

## 🔄 Pipeline de Implementación (Backend-First)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                FASE 0-1: INFRA + AUTH (✅ COMPLETADA)                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣ EZE → infra-setup ✅                                                 │
│  2️⃣ MATI → backend-config ✅                                            │
│  3️⃣ LUCAS → frontend-config ✅                                           │
│  4️⃣ LEANDRO → backend-patterns ✅                                        │
│  5️⃣ EDGAR → error-handling ✅                                           │
│  6️⃣ EZE → auth-backend ✅                                               │
│  7️⃣ MATI → auth-frontend ✅                                             │
│  8️⃣ LUCAS → categories-module ✅                                        │
│  9️⃣ EDGAR → ingredients-module ✅                                       │
│  🔟 LEANDRO → addresses-module ✅                                       │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                FASE 2: DOCKER + BACKEND PURO (🔄 EN PROGRESO)              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣1️⃣ EZE → docker-setup 🆕 ✅                                            │
│            ↓ (Docker Compose listo: PostgreSQL + backend + frontend)     │
│                                                                           │
│  1️⃣1️⃣🅱️ EZE → fix-backend-startup 🆕 ✅                                    │
│            ↓ (Fix: forward refs en routers + seed condicional)           │
│                                                                           │
│  1️⃣2️⃣ MATI → products-module (⏳ espera 8+9) ✅                            │
│            ↓ (CRUD productos + catálogo público)                         │
│                                                                           │
│  1️⃣3️⃣ LEANDRO → orders-fsm (⏳ espera 10+12) ✅                           │
│              ↓ (Pedidos + FSM básica)                                    │
│                                                                           │
│  1️⃣4️⃣ EZE → payments-integration (✅ 2026-05-12)                        │
│           ↓ (MercadoPago webhook)                                        │
│                                                                           │
│  1️⃣5️⃣ LEANDRO → orders-list-gestor (✅ 2026-05-13) 🔀                     │
│              ↓ (Router admin pedidos — solo backend)                     │
│                                                                           │
│  1️⃣6️⃣ EDGAR → users-admin (✅ 2026-05-13) 🔀                               │
│             ↓ (CRUD usuarios admin — solo backend)                       │
│                                                                           │
│  1️⃣7️⃣ EDGAR → admin-metrics (✅ 2026-05-13) 🔀                         │
│             ↓ (Endpoints métricas — solo backend)                        │
│                                                                           │
│  1️⃣7️⃣🅱️ EZE → auth-audit (✅ 2026-05-13) 🆕                                │
│             ↓ (Auditoría auth: 22 bugs, 48 tareas, HTTPBearer, apellido)  │
│                                                                           │
│  1️⃣7️⃣🅲️ EZE → bugfix-modules (✅ 2026-05-13) 🆕                            │
│             ↓ (CTE text(), categoria_padre_id, producto delete msg)       │
│                                                                           │
│  1️⃣7️⃣🅳️ LUCAS → verification-fixes (✅ Archivado 2026-05-13) 🆕                       │
│             ↓ (401→403 tests, categorias hierarchy, rate limit, pagos)    │
│                                                                           │
│  1️⃣7️⃣🅴️ EZE → auth-frontend-fix (✅ Archivado 2026-05-13) 🆕                      │
│             ↓ (snake_case auth, apellido register, perfil fetch, cart UI) │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                FASE 3: FRONTEND (🔒 CONSULTAR USUARIO)                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣8️⃣ LUCAS → cart-frontend (✅ Archivado 2026-05-13)                            │
│  1️⃣9️⃣ MATI → orders-list-client (✅ Archivado 2026-05-14)               │
│  2️⃣0️⃣ LUCAS → orders-list-gestor-frontend (✅ Archivado 2026-05-14) 🆕           │
│  2️⃣1️⃣ LUCAS → users-admin-frontend (✅ Archivado 2026-05-14) 🆕                   │
│  2️⃣2️⃣ LUCAS → admin-metrics-frontend (✅ Archivado 2026-05-14) 🆕           │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### 🔄 FASE 3b — Fixes y Auditorías (✅ COMPLETADA)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                FASE 3b: FIXES Y AUDITORÍAS (✅ COMPLETADA)                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  2️⃣4️⃣ EZE → fix-backend-startup (✅ Archivado 2026-05-08)                │
│  2️⃣5️⃣ EZE → auth-audit (✅ Archivado 2026-05-13)                         │
│  2️⃣6️⃣ EZE → bugfix-modules (✅ Archivado 2026-05-13)                     │
│  2️⃣7️⃣ LUCAS → verification-fixes (✅ Archivado 2026-05-13)               │
│  2️⃣8️⃣ EZE → auth-frontend-fix (✅ Archivado 2026-05-13)                  │
│  2️⃣9️⃣ EZE → audit-fixes (✅ Archivado 2026-05-14)                        │
│  3️⃣0️⃣ EZE → backend-security-fixes (✅ Archivado 2026-05-14)             │
│  3️⃣1️⃣ EZE → payments-audit-fixes (✅ Archivado 2026-05-14)               │
│  3️⃣2️⃣ EZE → frontend-integration-fixes (✅ Archivado 2026-05-14)         │
│  3️⃣3️⃣ EZE → docs-sync (✅ Archivado 2026-05-14)                          │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### 🔲 FASE 4 — Deuda Técnica (🔄 PARALELO — TODOS ARRANCAN JUNTOS)

```
┌──────────────────────────────────────────────────────────────────────────┐
│           FASE 4: DEUDA TÉCNICA (🔄 PARALELO — 2 changes c/u)            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─ EDGAR (Backend) ──────────────────────────────────────────────────┐  │
│  │  3️⃣4️⃣ backend-datetime-fix 🆕                                       │  │
│  │     ↓ (21 datetime.utcnow() → datetime.now(timezone.utc))          │  │
│  │                                                                     │  │
│  │  3️⃣5️⃣ backend-pydantic-modernize 🆕                                │  │
│  │     ↓ (class Config: → model_config = ConfigDict(...))             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌─ LUCAS (Frontend) ─────────────────────────────────────────────────┐  │
│  │  3️⃣6️⃣ frontend-home-page 🆕                                         │  │
│  │     ↓ (HomePage con catálogo destacado, hero, categorías)          │  │
│  │                                                                     │  │
│  │  3️⃣7️⃣ frontend-shared-ui 🆕                                         │  │
│  │     ↓ (Button, Input, Modal, Card en shared/ui/)                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌─ MATI (Frontend) ──────────────────────────────────────────────────┐  │
│  │  3️⃣8️⃣ frontend-profile-page 🆕                                      │  │
│  │     ↓ (ProfilePage para editar perfil y cambiar contraseña)        │  │
│  │                                                                     │  │
│  │  4️⃣3️⃣ frontend-orders-feature 🆕                                     │  │
│  │     ↓ (Mover OrdersPage de pages/ a features/orders/)              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌─ EZE (Backend) ────────────────────────────────────────────────────┐  │
│  │  4️⃣0️⃣ backend-refreshtokens 🆕                                      │  │
│  │     ↓ (Completar router.py, schemas.py, registrar en main.py)      │  │
│  │                                                                     │  │
│  │  4️⃣1️⃣ backend-admin-model 🆕                                        │  │
│  │     ↓ (Crear model.py de admin con queries reutilizables)          │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌─ LEANDRO (Frontend) ───────────────────────────────────────────────┐  │
│  │  4️⃣2️⃣ frontend-addresses-barrel 🆕                                   │  │
│  │     ↓ (Agregar index.ts barrel a entities/addresses/)              │  │
│  │                                                                     │  │
│  │  3️⃣9️⃣ frontend-fsd-restructure 🆕                                    │  │
│  │     ↓ (Mover providers/ dentro de app/)                            │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Orden de Implementación (Secuencial)

### ✅ COMPLETADOS (Fase 0-1)

| # | Orden | Integrante | Change | Depende de | Estado |
|---|-------|-----------|--------|-----------|--------|
| 1 | 1º | Eze | `infra-setup` | — | ✅ |
| 2 | 2º | Mati | `backend-config` | 1 | ✅ |
| 3 | 3º | Lucas | `frontend-config` | 1 | ✅ |
| 4 | 4º | Leandro | `backend-patterns` | 2 | ✅ |
| 5 | 5º | Edgar | `error-handling` | 4 | ✅ |
| 6 | 6º | Eze | `auth-backend` | 5 | ✅ |
| 7 | 7º | Mati | `auth-frontend` | 6,3 | ✅ |
| 8 | 7º | Lucas | `categories-module` | 6 | ✅ |
| 9 | 7º | Edgar | `ingredients-module` | 6 | ✅ |
| 10 | 8º | Leandro | `addresses-module` | 6 | ✅ |

### 🔲 FASE 2 — Docker + Backend Puro (🔄 EN PROGRESO)

| # | Orden | Integrante | Change | Depende de | Estado | ETA |
|---|-------|-----------|--------|-----------|--------|-----|
| 11 | **9º** | Eze | `docker-setup` 🆕 | 10 | ✅ | 0.5 días |
| 11b | **9º** | Eze | `fix-backend-startup` 🆕 | 11 | ✅ | 0.25 días |
| 12 | **10º** | Mati | `products-module` | 8,9 | ✅ | 1.5 días |
| 13 | **11º** | Leandro | `orders-fsm` | 10,12 | ✅ | 1.5 días |
| 14 | **12º** | Eze | `payments-integration` | 13 | ✅ Archivado 2026-05-12 | 1 día |
| 15 | **13º** | Leandro | `orders-list-gestor` 🔀 | 13 | ✅ Archivado 2026-05-13 | 0.5 días |
| 16 | **13º** | Edgar | `users-admin` 🔀 | 6 | ✅ Archivado 2026-05-13 | 1 día |
| 17 | **14º** | Edgar | `admin-metrics` 🔀 | 13,16 | ✅ Archivado 2026-05-13 | 1 día |
| 17b | **14º** | Eze | `auth-audit` 🆕 | 6 | ✅ Archivado 2026-05-13 | 1 día |
| 17c | **14º** | Eze | `bugfix-modules` 🆕 | 8,9,12 | ✅ Archivado 2026-05-13 | 0.5 días |
| 17d | **15º** | Lucas | `verification-fixes` 🆕 | 17b,17c | ✅ Archivado 2026-05-13 | 0.5 días |
| 17e | **15º** | Eze | `auth-frontend-fix` 🆕 | 17d | ✅ Archivado 2026-05-13 | 0.5 días |

> 📦 = Puede ejecutarse en paralelo con el cambio anterior (mismo padre terminado)  
> 🔀 = Cambio partido — solo backend en esta fase

### ✅ FASE 3 — Frontend (completada)

| # | Orden | Integrante | Change | Depende de | Estado | ETA |
|---|-------|-----------|--------|-----------|--------|-----|
| 18 | **15º** | Lucas | `cart-frontend` | 12 | ✅ Archivado 2026-05-13 | 1 día |
| 19 | **15º** | Mati | `orders-list-client` | 13 | ✅ Archivado 2026-05-14 | 0.5 días |
| 20 | **16º** | Lucas | `orders-list-gestor-frontend` 🆕 | 15 | ✅ Archivado 2026-05-14 | 0.5 días |
| 21 | **16º** | Lucas | `users-admin-frontend` 🆕 | 16 | ✅ Archivado 2026-05-14 | 1 día |
| 22 | **17º** | Lucas | `admin-metrics-frontend` 🆕 | 17 | ✅ Archivado 2026-05-14 | 1 día |
| 23 | **17º** | Eze | `checkout-frontend` 🆕 | 14, 18, 10 | ✅ Archivado 2026-05-14 | 1 día |

### ✅ FASE 3b — Fixes y Auditorías (completada)

| # | Orden | Integrante | Change | Depende de | Estado |
|---|-------|-----------|--------|-----------|--------|
| 24 | — | Eze | `fix-backend-startup` 🆕 | 11 | ✅ Archivado 2026-05-08 |
| 25 | — | Eze | `auth-audit` 🆕 | 6 | ✅ Archivado 2026-05-13 |
| 26 | — | Eze | `bugfix-modules` 🆕 | 8,9,12 | ✅ Archivado 2026-05-13 |
| 27 | — | Lucas | `verification-fixes` 🆕 | 25,26 | ✅ Archivado 2026-05-13 |
| 28 | — | Eze | `auth-frontend-fix` 🆕 | 27 | ✅ Archivado 2026-05-13 |
| 29 | — | Eze | `audit-fixes` 🆕 | 23 | ✅ Archivado 2026-05-14 |
| 30 | — | Eze | `backend-security-fixes` 🆕 | 6 | ✅ Archivado 2026-05-14 |
| 31 | — | Eze | `payments-audit-fixes` 🆕 | 14 | ✅ Archivado 2026-05-14 |
| 32 | — | Eze | `frontend-integration-fixes` 🆕 | 23 | ✅ Archivado 2026-05-14 |
| 33 | — | Eze | `docs-sync` 🆕 | — | ✅ Archivado 2026-05-14 |

### 🔲 FASE 4 — Deuda Técnica (paralelo — todos arrancan juntos)

| # | Integrante | Change | Qué hacer | Prioridad |
|---|-----------|--------|-----------|-----------|
| 34 | Edgar | `backend-datetime-fix` 🆕 | 21 `datetime.utcnow()` → `datetime.now(timezone.utc)` | 🟡 Media |
| 35 | Edgar | `backend-pydantic-modernize` 🆕 | `class Config:` → `model_config` en 5 schemas | 🟡 Media |
| 36 | Lucas | `frontend-home-page` 🆕 | HomePage con catálogo, hero, categorías | 🔴 Alta |
| 37 | Lucas | `frontend-shared-ui` 🆕 | Button, Input, Modal, Card en `shared/ui/` | ✅ Archivado 2026-05-15 |
| 38 | Mati | `frontend-profile-page` 🆕 | ProfilePage para editar perfil | 🟡 Media |
| 43 | Mati | `frontend-orders-feature` 🆕 | Mover OrdersPage a `features/orders/` | 🟢 Baja |
| 40 | Eze | `backend-refreshtokens` ✅ Archivado 2026-05-15 | Completar router.py, schemas.py, main.py | 🟢 Baja |
| 41 \| Eze \| `backend-admin-model` ✅ Archivado 2026-05-15 | Crear model.py de admin con queries | 🟢 Baja |
| 42 | Leandro | `frontend-addresses-barrel` 🆕 | Agregar index.ts a entities/addresses/ | 🟢 Baja |
| 39 | Leandro | `frontend-fsd-restructure` 🆕 | Mover providers/ dentro de app/ | 🟢 Baja |

> 🔄 **Todos arrancan en paralelo.** Cada change es independiente — nadie bloquea a nadie.

**Leyenda:**  
- ✅ = Completado y archivado
- 🔲 = Pendiente de implementar
- ⏳ = Espera a que el anterior esté archivado (MERGE)
- 📦 = Puede ejecutarse en paralelo (mismo padre)
- 🆕 = Change nuevo (no existía en v2.0)
- 🔀 = Change partido (solo backend en esta fase)
- 🔴 = Prioridad alta (UX crítica)
- 🟡 = Prioridad media (calidad de código)
- 🟢 = Prioridad baja (deuda técnica menor)

---

## Reglas de Coordinación (CRÍTICAS)

### ✅ Antes de empezar cada change

1. **Tu integrante anterior debe haber hecho MERGE** a `main`
2. Leer el `CHANGES-ROADMAP.md` completo (versión 2.1)
3. El código base que necesitas debe estar en `main` (hacer `git pull`)

### ✅ Durante implementación

1. Crear rama: `git checkout -b {change-name}` (ej: `products-module`)
2. Crear **proposal.md** → Review
3. Crear **design.md** → Review
4. Implementar cambios (tests incluidos)
5. Hacer commit: `feat(EPIC-XX): {change-name}` 

### ✅ Al terminar (ANTES de pasar al siguiente)

1. **Todo debe estar MERGEADO a `main`** (el siguiente depende de esto)
2. Avisar en Slack: "✅ {change} LISTO PARA {proximo_integrante}"
3. El siguiente hace `git pull` y empieza

### ❌ NUNCA

- ❌ Empezar si el anterior NO está en `main`
- ❌ Hacer commit sin tests
- ❌ Mezclar dos changes en un mismo PR
- ❌ Dejar ramas sin mergear
- ❌ **Tocar frontend en Fase 2** (solo backend puro)
- ❌ **Empezar Fase 3 sin consultar al usuario**

### 🆕 Reglas Backend-First

1. **Fase 2 es backend puro.** Si durante la implementación de un change de backend se detecta que se necesita un cambio en el frontend, se consulta al usuario
2. **Docker es opcional.** Si el equipo prefiere no usar Docker, se saltea el change 11 y cada integrante configura PostgreSQL localmente
3. **Cambios partidos (🔀):** `orders-list-gestor`, `users-admin` y `admin-metrics` ahora son solo backend. Su frontend se implementa en changes separados (20, 21, 22) durante la Fase 3
4. **Fase 3 completada:** Todos los changes de frontend están archivados
5. **Fase 4 (deuda técnica):** 2 changes por persona. Todos arrancan en paralelo — nadie bloquea a nadie. Cada change es independiente.

---

## Resumen Final

| Integrante | Completados | Pendientes (Fase 4) | Total |
|-----------|-----------|-------------------|-------|
| **Eze** | 1, 6, 11, 11b, 14, 17b, 17c, 17e, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 40 | 41 (`backend-admin-model`) | 20 ✅ + 0 🔲 \|
| **Mati** | 2, 7, 12, 19 | 38 (`frontend-profile-page`), 43 (`frontend-orders-feature`) | 4 ✅ + 0 🔲 \|
| **Lucas** | 3, 8, 18, 20, 21, 22, 27 | 36 (`frontend-home-page`), 37 (`frontend-shared-ui`) | 7 ✅ + 2 🔲 |
| **Edgar** | 5, 9, 16, 17 | 34 (`backend-datetime-fix`), 35 (`backend-pydantic-modernize`) | 4 ✅ + 0 🔲 \|
| **Leandro** | 4, 10, 13, 15 | 42 (`frontend-addresses-barrel`), 39 (`frontend-fsd-restructure`) | 4 ✅ + 0 🔲 \|

**Total:** 43 changes — 33 completados + 10 pendientes. **2 changes por persona, todos en paralelo.**

---

> **Fase actual:** ✅ FASES 0-3 COMPLETADAS (33/43 changes)  
> **Fase pendiente:** 🔲 FASE 4 — Deuda Técnica (10 changes)  
> **Último change completado:** `docs-sync` (Eze) ✅ 2026-05-14  
> **Última actualización:** 2026-05-14 — Sync de documentación v3.0

---

## 🔧 Pendientes de Verificación y Corrección — ✅ COMPLETADO

> **Asignado a: Lucas**  
> **Origen:** Auditoría `auth-audit` + verificación manual de endpoints  
> **Estado:** TODAS las tareas completadas el 2026-05-13.

### 1. Actualizar tests con expectativas 401 → 403

`HTTPBearer` (reemplazo de `OAuth2PasswordBearer`) devuelve **403** en vez de **401** cuando no hay token. Tests que esperan 401 deben actualizarse:

| Archivo | Tests afectados |
|---------|-----------------|
| `tests/modules/pedidos/test_pedidos_endpoints.py` | ~8 tests esperan 401 → deben esperar 403 |
| `tests/modules/admin/test_admin_metrics.py` | ~6 tests esperan 401 → deben esperar 403 |

### 2. Revisar tests de categorías hierarchy

3 tests en `tests/modules/categorias/test_hierarchy.py` fallan con 404:
- `test_move_category_to_different_branch`
- `test_public_tree_no_auth`
- `test_leaf_category_subcategorias`

Posible causa: rutas incorrectas o endpoints no implementados.

### 3. Schemas de update verificados ✅

Todos los schemas de UPDATE tienen campos opcionales (`default=None`). Sin cambios necesarios.

### 4. Rate limiting: 5/min vs 5/15min

El código tiene `5/minute` (config.py default) pero los docs dicen `5/15min`. Evaluar cuál usar y unificar.

### 5. Pagos y Admin endpoints

Marcados PENDIENTE en verificación manual. Probar flujo completo de pago con MercadoPago y dashboard admin.

### 6. Cambios archivados

| Change | Archivo |
|--------|---------|
| `auth-audit` | `openspec/changes/archive/2026-05-13-auth-audit/` (48/48 tareas) |
| `bugfix-modules` | `openspec/changes/archive/2026-05-13-bugfix-modules/` (12/12 tareas) |

---

> **Última actualización:** 2026-05-14 — Eze (checkout-frontend)
