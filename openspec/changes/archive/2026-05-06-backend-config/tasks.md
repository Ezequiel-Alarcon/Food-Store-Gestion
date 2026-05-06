## 1. Configuración de Proyecto

- [x] 1.1 Crear backend/app/core/config.py con pydantic-settings
- [x] 1.2 Crear backend/app/core/database.py con SQLModel engine y SessionLocal
- [x] 1.3 Crear backend/app/core/security.py con bcrypt y JWT utils
- [x] 1.4 Crear backend/requirements.txt con todas las dependencias

## 2. FastAPI App

- [x] 2.1 Crear backend/app/main.py con app FastAPI
- [x] 2.2 Configurar CORS con orígenes desde settings
- [x] 2.3 Configurar slowapi rate limiting (5 intentos/15min en login)
- [x] 2.4 Agregar exception handlers RFC 7807
- [x] 2.5 Incluir routers de módulos (auth, usuarios, productos, etc.)

## 3. Alembic

- [x] 3.1 Inicializar Alembic con alembic init backend/app/db/migrations
- [x] 3.2 Configurar alembic.ini con database URL desde settings
- [x] 3.3 Configurar backend/app/db/migrations/env.py para importar modelos
- [x] 3.4 Crear backend/app/models/__init__.py re-exportando todos los modelos
- [ ] 3.5 Generar migración inicial con alembic revision --autogenerate (pendiente: requiere modelos SQLModel en módulos)

## 4. Seed Data

- [x] 4.1 Crear backend/app/db/seed.py con función run_seed()
- [x] 4.2 Insertar Roles (ADMIN, STOCK, PEDIDOS, CLIENT)
- [x] 4.3 Insertar EstadosPedido (6 estados con es_terminal)
- [x] 4.4 Insertar FormaPago (MERCADOPAGO, EFECTIVO, TRANSFERENCIA)
- [x] 4.5 Crear usuario admin@foodstore.com con bcrypt cost 12

## 5. Archivos de Entorno

- [x] 5.1 Crear .env.example con DATABASE_URL, SECRET_KEY, etc.
- [x] 5.2 Crear .env de desarrollo con valores locales