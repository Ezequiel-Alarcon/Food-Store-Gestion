# Food Store — Asignación por Team (Pipeline Backend-First)

> **Proyecto:** Food Store E-Commerce  
> **Fecha:** 2026-05-13  
> **Distribución:** 22 changes entre 5 integrantes  
> **Método:** Secuencial con fases Backend → Frontend  
> **Versión:** 2.1 (reordenamiento backend-first)

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
│  1️⃣7️⃣🅳️ LUCAS → verification-fixes (🔲 PENDIENTE) 🆕                       │
│             ↓ (401→403 tests, categorias hierarchy, rate limit, pagos)    │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                FASE 3: FRONTEND (🔒 CONSULTAR USUARIO)                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣8️⃣ LUCAS → cart-frontend 🔒 (⏳ espera 12)                            │
│  1️⃣9️⃣ MATI → orders-list-client 🔒 (⏳ espera 13)                       │
│  2️⃣0️⃣ LUCAS → orders-list-gestor-frontend 🔒 (⏳ espera 15) 🆕           │
│  2️⃣1️⃣ MATI → users-admin-frontend 🔒 (⏳ espera 16) 🆕                   │
│  2️⃣2️⃣ LUCAS → admin-metrics-frontend 🔒 (⏳ espera 17) 🆕                │
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
| 17d | **15º** | Lucas | `verification-fixes` 🆕 | 17b,17c | 🔲 Pendiente | 0.5 días |

> 📦 = Puede ejecutarse en paralelo con el cambio anterior (mismo padre terminado)  
> 🔀 = Cambio partido — solo backend en esta fase

### 🔒 FASE 3 — Frontend (consultar antes de cada uno)

| # | Orden | Integrante | Change | Depende de | Estado | ETA |
|---|-------|-----------|--------|-----------|--------|-----|
| 18 | **15º** | Lucas | `cart-frontend` 🔒 | 12 | 🔒 | 1 día |
| 19 | **15º** | Mati | `orders-list-client` 🔒 | 13 | 🔒 | 0.5 días |
| 20 | **16º** | Lucas | `orders-list-gestor-frontend` 🆕 🔒 | 15 | 🔒 | 0.5 días |
| 21 | **16º** | Mati | `users-admin-frontend` 🆕 🔒 | 16 | 🔒 | 1 día |
| 22 | **17º** | Lucas | `admin-metrics-frontend` 🆕 🔒 | 17 | 🔒 | 1 día |

> 🔒 = **NO implementar sin consulta explícita al usuario.**  
> La Fase 3 no arranca automáticamente al terminar la Fase 2.

**Leyenda:**  
- ✅ = Completado y archivado
- ⏳ = Espera a que el anterior esté archivado (MERGE)
- 📦 = Puede ejecutarse en paralelo (mismo padre)
- 🔒 = Requiere consulta al usuario antes de empezar
- 🆕 = Change nuevo (no existía en v2.0)
- 🔀 = Change partido (solo backend en esta fase)

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
4. **Fase 3 bloqueada:** Nadie arranca un change de frontend sin que el usuario dé el visto bueno explícito

---

## Resumen Final

| Integrante | Changes | Total HU | Cambios nuevos | Rol |
|-----------|---------|----------|---------------|-----|
| **Eze** | 1, 6, 11, 11b, 14, 17b, 17c | 12 + docker + fixes | `docker-setup` 🆕, `fix-backend-startup` 🆕, `auth-audit` 🆕, `bugfix-modules` 🆕 | Infra + Auth + Docker + Pagos + Fixes |
| **Mati** | 2, 7, 12, 19, 21 | 21 | `users-admin-frontend` 🆕 | Backend + Auth-FE + Productos + Orders-client + Admin-FE |
| **Lucas** | 3, 8, 18, 20, 22, 17d | 10 + 1 fix | `orders-list-gestor-frontend` 🆕, `admin-metrics-frontend` 🆕, `verification-fixes` 🆕 | Frontend + Categorías + Carrito + Admin-FE + Fixes |
| **Edgar** | 5, 9, 16, 17 | 16 | — | Errores + Ingredientes + Users-admin + Metrics |
| **Leandro** | 4, 10, 13, 15 | 15 | `orders-list-gestor` (backend) 🔀 | Patrones + Direcciones + FSM + Admin-pedidos |

**Total:** 25 changes, 77 HU, ~4-5 semanas (Fase 2: ~2 semanas, Fase 3: ~2 semanas)

---

> **Fase actual:** Fase 2 — Backend Puro  
> **Último change completado:** `admin-metrics` (Edgar) ✅ 2026-05-13
> **Regla de oro:** Backend first, frontend after — siempre consultar antes de tocar frontend.

---

## 📝 Notas para el equipo (2026-05-08)

### Cambios aplicados en `fix-backend-startup` (Eze)

1. **`from __future__ import annotations` eliminado de TODOS los `router.py`** (8 archivos: auth, sucursales, ingredientes, direcciones, categorias, usuarios, perfil, patterns_example). Causaba que Pydantic v2 no resolviera los tipos al decorar rutas FastAPI → `NameError: name 'LoginRequest' is not defined`.

2. **`db/seed.py` con imports condicionales.** Los modelos `Rol`, `UsuarioRol`, `EstadoPedido`, `FormaPago` se importan con `try/except ImportError`. Si el modelo no existe aún (changes futuros no implementados), el seed omite esa parte sin crashear.

3. **`requirements.txt` corregido** (parte de docker-setup): eliminado `python-cors==1.3.5` (no existe en PyPI), actualizado `python-multipart==0.0.6` → `0.0.7` (requerido por FastAPI 0.111).

4. **Migraciones corregidas** (parte de docker-setup): dos revisiones `003` duplicadas → una renumerada a `004`.

### Para el próximo que implemente (`products-module` — Mati)

- El backend arranca con `docker compose up`. Probar después de hacer `git pull`.
- Los modelos `Usuario` y `UsuarioRol` YA existen en `app/modules/auth/model.py`. Al implementar `Rol`, el seed lo va a poblar automáticamente.
- Si necesitás tocar `seed.py` para agregar productos de ejemplo, seguí el patrón de imports condicionales.

---

## 🔧 Pendientes de Verificación y Corrección (2026-05-13)

> **Asignado a: Lucas**  
> **Origen:** Auditoría `auth-audit` + verificación manual de endpoints  
> **Contexto:** Se completaron 2 changes correctivos (auth-audit y bugfix-modules). Quedan tareas de verificación y ajustes en tests.

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

> **Última actualización:** 2026-05-13 — Eze (auth-audit + bugfix-modules)
