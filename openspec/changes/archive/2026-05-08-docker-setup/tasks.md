## 0. Cross-platform Setup

- [x] 0.1 Crear o actualizar `.gitattributes` en la raíz con `* text=auto` y forzar LF para scripts: `*.sh text eol=lf`, `Dockerfile text eol=lf`, `*.yml text eol=lf`

## 1. Backend Dockerfile

- [x] 1.1 Crear `backend/.dockerignore` excluyendo `.venv`, `__pycache__`, `.git`, `*.pyc`, `.env`, `.mypy_cache`, `.pytest_cache`, `.coverage`, `htmlcov`, archivos de IDE
- [x] 1.2 Crear `backend/Dockerfile` multi-stage: stage `base` con `python:3.11-slim`, copiar `requirements.txt`, instalar dependencias con `pip --no-cache-dir`
- [x] 1.3 Agregar stage `dev` en el Dockerfile: hereda de `base`, expone puerto 8000, usa entrypoint script
- [x] 1.4 Agregar stage `prod` en el Dockerfile: hereda de `base`, copia código, instala gunicorn, usa `gunicorn` con `uvicorn.workers.UvicornWorker`
- [x] 1.5 Crear `backend/docker-entrypoint.sh`: espera a PostgreSQL usando `psycopg2` (bucle con sleep 2s, timeout 60s con exit code ≠ 0), ejecuta `alembic upgrade head`, ejecuta `python -m app.db.seed`, arranca uvicorn con `exec`
- [x] 1.6 Hacer ejecutable `docker-entrypoint.sh` (`chmod +x` en el Dockerfile) y usar `ENTRYPOINT` en modo `exec`

## 2. Frontend Dockerfile

- [x] 2.1 Crear `frontend/.dockerignore` excluyendo `node_modules`, `dist`, `.git`, `.env`, `.env.local`, `coverage`, archivos de IDE
- [x] 2.2 Crear `frontend/Dockerfile` multi-stage: stage `base` con `node:18-alpine`, copiar `package*.json`, ejecutar `npm ci`
- [x] 2.3 Agregar stage `dev` en el Dockerfile: hereda de `base`, expone puerto 5173, ejecuta `npm run dev -- --host 0.0.0.0`
- [x] 2.4 Agregar stages `build` y `prod` como comentarios documentados: `tsc && vite build` → nginx:alpine sirviendo `/app/dist`

## 3. Vite Proxy Configuration

- [x] 3.1 Modificar `frontend/vite.config.ts`: usar `VITE_BACKEND_URL` como target del proxy si está definida, con fallback a `http://localhost:8000`

## 4. Environment Variables

- [x] 4.1 Crear `.env` en la raíz del proyecto con: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL` (host=db), `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `CORS_ORIGINS`, `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY`, `DEBUG`, `ENVIRONMENT`, `VITE_API_URL`, `VITE_MP_PUBLIC_KEY`, `VITE_BACKEND_URL`

## 5. Docker Compose

- [x] 5.1 Crear `docker-compose.yml` en la raíz: servicio `db` con `postgres:15-alpine`, variables de entorno desde `.env`, healthcheck con `pg_isready`, volumen `pg_data`, puerto `5432`
- [x] 5.2 Agregar servicio `backend`: build desde `./backend` con `target: dev`, depends_on `db` con `condition: service_healthy`, bind mount `./backend/app:/app/app` para hot reload, puerto `8000`, variables de entorno desde `.env`
- [x] 5.3 Agregar servicio `frontend`: build desde `./frontend` con `target: dev`, depends_on `backend`, bind mount `./frontend/src:/app/src` para hot reload, puerto `5173`, variables de entorno desde `.env`
- [x] 5.4 Definir volumen `pg_data` en la sección `volumes` de docker-compose

## 6. Verification

- [x] 6.1 Ejecutar `docker compose build` y verificar que los 3 servicios compilan sin errores
- [x] 6.2 Ejecutar `docker compose up` y verificar: backend espera a PostgreSQL, migraciones corren, seed ejecuta, frontend accesible en `localhost:5173`
- [ ] 6.3 Verificar persistencia: crear datos (registrar usuario), `docker compose down`, `docker compose up`, verificar que los datos persisten
- [x] 6.4 Verificar compatibilidad sin Docker: `npm run dev` en frontend y `uvicorn app.main:app` en backend siguen funcionando con PostgreSQL local
