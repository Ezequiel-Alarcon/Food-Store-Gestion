## Why

El proyecto requiere que cada desarrollador configure manualmente Python 3.11, Node.js 18, y PostgreSQL 15 en su máquina local. Esto genera fricción de onboarding, inconsistencias de entorno ("en mi máquina funciona"), y no existe un camino hacia el despliegue productivo. Dockerizar ahora garantiza entornos idénticos para todo el equipo y sienta las bases para CI/CD futuro.

## What Changes

- Crear `Dockerfile` multi-stage para el backend (targets: `base`, `dev`, `prod`) usando `python:3.11-slim`
- Crear `Dockerfile` multi-stage para el frontend (targets: `base`, `dev`, con placeholder para `prod`) usando `node:18-alpine`
- Crear `docker-compose.yml` en la raíz orquestando los 3 servicios: `frontend`, `backend`, `db` (PostgreSQL 15)
- Crear `docker-entrypoint.sh` para el backend: espera a PostgreSQL → migraciones Alembic → seed → uvicorn
- Crear `.dockerignore` para backend y frontend (excluir `node_modules`, `.venv`, `__pycache__`, `.git`)
- Crear `.env` raíz unificado con variables de entorno para Docker
- Modificar `frontend/vite.config.ts`: proxy de `localhost:8000` → `backend:8000` cuando corre en Docker (condicional por variable de entorno)

## Capabilities

### New Capabilities

- `docker-backend`: Containerización del backend FastAPI con espera de base de datos, migraciones automáticas, seed data, y hot reload en desarrollo. Targets dev y prod en un solo Dockerfile.
- `docker-frontend`: Containerización del frontend React + Vite con hot reload en desarrollo, proxy configurable al backend, y placeholder preparado para build productivo con Nginx.
- `docker-orchestration`: Orquestación de los 3 servicios (frontend, backend, PostgreSQL) mediante docker-compose, con dependencias de arranque, healthchecks, volúmenes para persistencia de datos, y bind mounts para desarrollo.

### Modified Capabilities

Ninguna. Este change no modifica requisitos de specs existentes — solo agrega containerización sin alterar el comportamiento funcional de la aplicación.

## Impact

- **Archivos nuevos**:
  - `docker-compose.yml` — orquestación de servicios
  - `.env` — variables de entorno unificadas para Docker
  - `backend/Dockerfile` — multi-stage (base, dev, prod)
  - `backend/docker-entrypoint.sh` — script de inicialización
  - `backend/.dockerignore` — exclusiones de build context
  - `frontend/Dockerfile` — multi-stage (base, dev, prod placeholder)
  - `frontend/.dockerignore` — exclusiones de build context
- **Archivos modificados**: `frontend/vite.config.ts` — proxy dinámico según entorno
- **Dependencias externas**: Docker Engine + Docker Compose (ya disponibles en el sistema)
- **Sin breaking changes**: los setups locales sin Docker siguen funcionando idénticamente
