## Context

Food Store es un monorepo con backend FastAPI + PostgreSQL y frontend React + Vite. Actualmente cada desarrollador configura su entorno manualmente (Python venv, Node.js, PostgreSQL local). No existe containerización, lo que genera inconsistencias entre entornos, fricción de onboarding, y ausencia de un camino hacia CI/CD y despliegue.

El equipo ya tiene Docker Engine y Docker Compose instalados. Las dependencias del proyecto están declaradas en `backend/requirements.txt` y `frontend/package.json`. La configuración de entorno usa `.env.example` por servicio.

## Goals / Non-Goals

**Goals:**
- Un solo comando levanta todo: `docker compose up`
- Backend: espera a PostgreSQL, ejecuta migraciones, seed, y arranca con hot reload
- Frontend: Vite dev server con hot reload y proxy al backend
- PostgreSQL: datos persistentes en volumen, healthcheck para dependencias
- Desarrollo local sin Docker sigue funcionando sin cambios
- Un solo Dockerfile por servicio, con targets `dev`/`prod`
- Un solo `.env` raíz para todas las variables de Docker

**Non-Goals:**
- Build productivo con Nginx para frontend (placeholder preparado, no implementado)
- Multi-architecture builds (arm64/amd64)
- Docker Swarm o Kubernetes
- CI/CD pipeline (sienta las bases, no lo implementa)
- Secrets management para producción (.env en desarrollo es suficiente)

## Decisions

### 1. Entrada única: `.env` raíz en vez de múltiples `.env`

**Elegido**: Un `.env` en la raíz del proyecto con todas las variables de entorno para Docker Compose.

**Alternativa considerada**: Mantener `backend/.env` y `frontend/.env` separados con `env_file:` por servicio.

**Razón**: docker-compose lee un solo `.env` por defecto. Variables como `DATABASE_URL` son compartidas (backend la usa para conectarse; el servicio `db` la deriva de `POSTGRES_USER/PASSWORD/DB`). Centralizar evita divergencia entre archivos. Los `.env.example` existentes se mantienen como documentación para desarrollo sin Docker.

### 2. Entrypoint en Bash, no en Python ni dependencias externas

**Elegido**: Script `docker-entrypoint.sh` que espera a PostgreSQL usando `psycopg2` (ya instalado), ejecuta migraciones, seed, y arranca uvicorn con `exec`.

**Alternativa considerada**: Usar `wait-for-it.sh`, `pg_isready`, o un script en Python.

**Razón**: `psycopg2` ya es dependencia del proyecto — no agrega overhead. `pg_isready` requiere `postgresql-client` en la imagen (≈50MB extra). `wait-for-it.sh` es un binario externo más. Bash con `exec` asegura que uvicorn sea PID 1 y reciba señales de shutdown correctamente.

### 3. Multi-stage Dockerfile: un archivo, dos targets

**Elegido**: Un solo `Dockerfile` por servicio con stages `base`, `dev`, `prod`.

**Alternativa considerada**: `Dockerfile.dev` + `Dockerfile.prod` separados.

**Razón**: El stage `base` instala dependencias una sola vez; `dev` y `prod` heredan. Si se actualiza `requirements.txt`, ambos targets lo reflejan. Evita duplicación y divergencia entre archivos. El `docker-compose.yml` selecciona el target con `target: dev`.

### 4. Frontend: solo target dev, prod como placeholder comentado

**Elegido**: Implementar solo `dev`; documentar la estructura para `prod` con Nginx como comentarios en el Dockerfile.

**Alternativa considerada**: Implementar `dev` y `prod` completos desde el día 1.

**Razón**: El proyecto está en desarrollo activo (routers comentados, módulos sin implementar). Construir el target `prod` ahora sería arquitectura especulativa. La estructura del Dockerfile queda preparada para que agregar `prod` sea trivial cuando se necesite.

### 5. Proxy de Vite dinámico por variable de entorno

**Elegido**: Modificar `vite.config.ts` para que el target del proxy use `VITE_BACKEND_URL` si está definida, con fallback a `http://localhost:8000`.

**Alternativa considerada**: Mantener el proxy hardcodeado a `localhost:8000` y usar `VITE_API_URL` en el frontend.

**Razón**: El proxy de Vite es solo para desarrollo. En Docker, el backend está en `http://backend:8000` (nombre del servicio en la red de compose). Con una variable de entorno condicional, el mismo `vite.config.ts` funciona en ambos entornos sin bifurcaciones.

### 6. PostgreSQL: volumen nombrado para persistencia

**Elegido**: Volumen Docker nombrado (`pg_data`) gestionado por Compose.

**Alternativa considerada**: Bind mount a un directorio local (`./data/postgres`).

**Razón**: Los volúmenes nombrados son portables entre sistemas operativos, no requieren que el directorio exista previamente, y Docker gestiona permisos automáticamente. Un bind mount a `./data/` en Windows puede tener problemas de permisos con el filesystem de PostgreSQL.

### 7. `.dockerignore`: exclusiones agresivas

**Elegido**: Excluir `.venv`, `node_modules`, `__pycache__`, `.git`, `*.pyc`, `.env`, `dist`, `coverage`, y archivos de IDE.

**Razón**: Reduce el build context que Docker envía al daemon. Sin `.dockerignore`, `node_modules` y `.venv` se copian al contexto (cientos de MB), haciendo builds lentos y la imagen innecesariamente grande.

## Risks / Trade-offs

- **[Riesgo] El entrypoint falla si `psycopg2` se elimina de requirements.txt** → Mitigación: `psycopg2-binary` es la dependencia de PostgreSQL del proyecto — no se va a eliminar. Si cambia, el Dockerfile se actualiza.
- **[Riesgo] Hot reload puede no detectar cambios en Windows con WSL2** → Mitigación: Vincular volúmenes con `:cached` o `:delegated` según el filesystem. Documentar en README.
- **[Riesgo] El proxy de Vite no reenvía WebSocket para HMR** → Mitigación: Vite configura `server.hmr` automáticamente en modo dev. Si hay problemas, se configura explícitamente `server.watch` con polling.
- **[Trade-off] `.env` raíz unificado vs `.env` por servicio** → Si el proyecto crece mucho, las variables pueden mezclarse. Solución futura: prefijos (`BACKEND_`, `DB_`, `FRONTEND_`). Por ahora, con ~15 variables, no es problema.
