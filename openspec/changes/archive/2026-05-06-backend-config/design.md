## Context

El change 1 (infra-setup) estableció la estructura del monorepo feature-first. El change 2 (backend-config) implementa la capa de infraestructura del backend: FastAPI app, conexión a PostgreSQL, migraciones Alembic y datos iniciales.

Este change es prerequisito para todos los módulos de negocio porque:
- Sin main.py no hay forma de levantar el servidor
- Sin database.py no hay conexión a PostgreSQL
- Sin Alembic no se pueden crear las tablas
- Sin seed data los módulos no funcionan (ej: no hay Roles para RBAC)

## Goals / Non-Goals

**Goals:**
1. FastAPI app funcionando con CORS, rate limiting, exception handlers RFC 7807
2. Conexión SQLModel a PostgreSQL con engine y session factory
3. Alembic configurado con migrations/ y alembic.ini
4. Seed data ejecutable: Roles (ADMIN, STOCK, PEDIDOS, CLIENT), EstadosPedido (6 estados), FormaPago (3 formas), usuario admin@foodstore.com

**Non-Goals:**
- No implementar lógica de negocio (módulos)
- No implementar auth ni protección de rutas
- No crear las tablas de los módulos (eso lo hace Alembic desde los modelos)

## Decisions

### D1: Pydantic Settings para configuración
**Alternativas consideradas:** Variables de entorno directas, .env file manual, yaml config
**Elección:** Pydantic Settings (`pydantic-settings`) con `.env` file
**Rationale:** Tipado automático, validación, integración nativa con FastAPI. Permite `Settings().DATABASE_URL` con autocomplete.

### D2: SQLModel Engine como singleton de conexión
**Alternativas consideradas:** create_engine clásico, async engine, connection pool manual
**Elección:** SQLModel create_engine con SessionLocal
**Rationale:** SQLModel unifica SQLAlchemy + Pydantic. SessionLocal permite el patrón UoW con `Session()` contexto.

### D3: Alembic con --autogenerate
**Alternativas consideradas:** Migraciones manuales, SQLModel metaclass
**Elección:** Alembic con revisión inicial + autogenerate desde modelos
**Rationale:** Es el estándar de la industria para PostgreSQL. Autogenerate infiere cambios de los modelos SQLModel.

### D4: bcrypt cost 12
**Alternativas consideradas:** cost 10 (más rápido), cost 14 (más seguro)
**Elección:** cost 12 (default de Passlib)
**Rationale:** Equilibrio entre seguridad y performance.-documented en Integrador.txt.

### D5: slowapi para rate limiting
**Alternativas consideradas:** flask-limiter, nginx, custom middleware
**Elección:** slowapi con límite 5 intentos/15min en login
**Rationale:** Integración nativa con FastAPI, compatible con dependency injection.

## Risks / Trade-offs

**[R1]** → Seed data debe ejecutarse DESPUÉS de Alembic
- Mitigation: Documentar en README y checklist de deployment

**[R2]** → Modelos en módulos deben importarse en alembic/env.py
- Mitigation: Crear backend/app/models/__init__.py que re-exporta todos los modelos

**[R3]** → CORS origins configurable por env
- Mitigation: CORS_ORIGINS como JSON array en .env, parsear en main.py