#!/bin/bash
set -e

# ── Colores para logs ──────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  Food Store Backend — Docker Entrypoint  ${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ── Esperar a PostgreSQL ───────────────────────────────────────────────
echo -e "\n${YELLOW}[1/4]${NC} Esperando a PostgreSQL en ${DATABASE_URL}..."
TIMEOUT=60
ELAPSED=0

until python -c "
import psycopg2
import os
url = os.environ['DATABASE_URL']
conn = psycopg2.connect(url)
conn.close()
print('OK')
" 2>/dev/null; do
    sleep 2
    ELAPSED=$((ELAPSED + 2))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo -e "${RED}✗ Timeout: PostgreSQL no disponible después de ${TIMEOUT}s${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓${NC} PostgreSQL listo (${ELAPSED}s)"

# ── Migraciones ─────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[2/4]${NC} Ejecutando migraciones Alembic..."
alembic upgrade head
echo -e "${GREEN}✓${NC} Migraciones completadas"

# ── Seed ─────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[3/4]${NC} Ejecutando seed de datos..."
python -m app.db.seed || echo -e "${YELLOW}⚠${NC} Seed omitido (modelos no implementados aún — normal en desarrollo)"
echo -e "${GREEN}✓${NC} Seed completado"

# ── Iniciar servidor ────────────────────────────────────────────────────
echo -e "\n${YELLOW}[4/4]${NC} Iniciando uvicorn..."
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  API: http://localhost:8000              ${NC}"
echo -e "${GREEN}  Docs: http://localhost:8000/docs         ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
