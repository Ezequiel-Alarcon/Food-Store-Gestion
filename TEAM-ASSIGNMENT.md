# Food Store — Asignación por Team (Pipeline Secuencial)

> **Proyecto:** Food Store E-Commerce  
> **Fecha:** 2026-05-06  
> **Distribución:** 18 changes entre 5 integrantes  
> **Método:** Secuencial — cada persona espera a que la anterior termine

---

## 🔄 Pipeline de Implementación (Orden Estricto)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          INFRAESTRUCTURA                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣ EZE → infra-setup                                                   │
│           ↓ (EZE termina, comparte código)                              │
│                                                                           │
│  2️⃣ MATI → backend-config                                              │
│            ↓ (MATI termina, comparte modelos SQLModel)                 │
│                                                                           │
│  3️⃣ LUCAS → frontend-config (📦 paralelo a 2, mismo padre)             │
│            ↓ (LUCAS termina, lista Vite)                               │
│                                                                           │
│  4️⃣ EDGAR → backend-patterns                                            │
│            ↓ (EDGAR termina, BaseRepository + UoW listos)              │
│                                                                           │
│  5️⃣ LEANDRO → error-handling                                            │
│              ↓ (LEANDRO termina, middleware + exceptions listos)        │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                   AUTENTICACIÓN Y PERMISOS                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  6️⃣ EZE → auth-backend                                                  │
│           ↓ (EZE termina, auth endpoints listos)                       │
│                                                                           │
│  7️⃣ MATI → auth-frontend (📦 paralelo a 8,9,10,11)                    │
│  8️⃣ LUCAS → categories-module (📦 paralelo a 7,9,10,11)               │
│  9️⃣ EDGAR → ingredients-module (📦 paralelo a 7,8,10,11)              │
│  🔟 LEANDRO → addresses-module (📦 paralelo a 7,8,9,11)               │
│  1️⃣1️⃣ EZE → products-module (❌ NO: depende de 8+9)                   │
│                                                                           │
│  [Todos reportan DONE]                                                   │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                        CATÁLOGO + PRODUCTOS                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣1️⃣ MATI → products-module (⏳ espera 8+9)                           │
│            ↓ (MATI termina, CRUD productos listo)                       │
│                                                                           │
│  1️⃣2️⃣ LUCAS → cart-frontend (⏳ espera 3+11)                            │
│            ↓ (LUCAS termina, carrito listo)                             │
│                                                                           │
│  1️⃣7️⃣ EDGAR → users-admin (⏳ espera 6)                                 │
│             ↓ (EDGAR termina, admin RBAC listo)                        │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                        PEDIDOS + PAGOS                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1️⃣3️⃣ LEANDRO → orders-fsm (⏳ espera 10+11)                            │
│              ↓ (LEANDRO termina, FSM pedidos lista)                     │
│                                                                           │
│  1️⃣4️⃣ EZE → payments-integration (⏳ espera 13)                         │
│           ↓ (EZE termina, MercadoPago integrado)                        │
│                                                                           │
│  1️⃣5️⃣ MATI → orders-list-client (📦 paralelo a 16)                     │
│  1️⃣6️⃣ LUCAS → orders-list-gestor (📦 paralelo a 15)                    │
│                                                                           │
│  [Ambos reportan DONE]                                                   │
│                                                                           │
│  1️⃣8️⃣ EDGAR → admin-metrics (⏳ espera 13+17)                           │
│             ↓ (EDGAR termina, dashboard KPIs listo)                    │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Orden de Implementación (Secuencial)

| # | Orden | Integrante | Change | Depende de | Estado | ETA |
|---|-------|-----------|--------|-----------|--------|-----|
| 1 | **1º** | Eze | `infra-setup` | — | ⏳ | 1 día |
| 2 | **2º** | Mati | `backend-config` | 1 | ⏳ | 1 día |
| 3 | **3º** | Lucas | `frontend-config` | 1 | 📦 | 1 día |
| 4 | **4º** | Edgar | `backend-patterns` | 2 | ⏳ | 0.5 días |
| 5 | **5º** | Leandro | `error-handling` | 4 | ⏳ | 0.5 días |
| 6 | **6º** | Eze | `auth-backend` | 5 | ⏳ | 1.5 días |
| 7 | **7º** | Mati | `auth-frontend` | 6,3 | 📦 | 1 día |
| 8 | **7º** | Lucas | `categories-module` | 6 | 📦 | 1 día |
| 9 | **7º** | Edgar | `ingredients-module` | 6 | 📦 | 0.5 días |
| 10 | **7º** | Leandro | `addresses-module` | 6 | 📦 | 1 día |
| 11 | **8º** | Mati | `products-module` | 8,9 | ⏳ | 1.5 días |
| 12 | **9º** | Lucas | `cart-frontend` | 3,11 | ⏳ | 1 día |
| 17 | **10º** | Edgar | `users-admin` | 6 | ⏳ | 0.5 días |
| 13 | **11º** | Leandro | `orders-fsm` | 10,11 | ⏳ | 1.5 días |
| 14 | **12º** | Eze | `payments-integration` | 13 | ⏳ | 1 día |
| 15 | **13º** | Mati | `orders-list-client` | 13 | 📦 | 0.5 días |
| 16 | **13º** | Lucas | `orders-list-gestor` | 13 | 📦 | 1 día |
| 18 | **14º** | Edgar | `admin-metrics` | 13,17 | ⏳ | 1.5 días |

**Leyenda:**  
- ⏳ = Espera a que el anterior esté archivado (MERGE)
- 📦 = Puede ejecutarse en paralelo (mismo padre)
- **Total secuencial:** ~14-15 días efectivos (3 semanas)

---

## Reglas de Coordinación (CRÍTICAS)

### ✅ Antes de empezar cada change

1. **Tu integrante anterior debe haber hecho MERGE** a `main`
2. Leer el `CHANGES-ROADMAP.md` completo
3. El código base que necesitas debe estar en `main` (hacer `git pull`)

### ✅ Durante implementación

1. Crear rama: `git checkout -b {change-name}` (ej: `auth-backend`)
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

---

## Resumen Final

| Integrante | Changes | Total HU | Duración | Rol |
|-----------|---------|----------|----------|-----|
| **Eze** | 1, 6, 14 | 9 | +3 semanas | Infra + Auth + Pagos |
| **Mati** | 2, 7, 11, 15 | 17 | +4.5 semanas | Backend + Auth-FE + Productos + Orders-client |
| **Lucas** | 3, 8, 12, 16 | 14 | +4 semanas | Frontend + Categorías + Carrito + Orders-gestor |
| **Edgar** | 4, 9, 17, 18 | 15 | +4 semanas | Patrones + Ingredientes + Users-admin + Metrics |
| **Leandro** | 5, 10, 13 | 10 | +3.5 semanas | Errores + Direcciones + FSM |

**Total:** 18 changes, 77 HU, ~3-4 semanas (asumiendo 1-2 días/change)

---

> **Cada integrante conoce exactamente cuándo es su turno y de quién depende.**  
> **El siguiente no puede empezar hasta que el anterior haya mergado a `main`.**
