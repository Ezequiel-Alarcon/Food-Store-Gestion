# ── Stage: base ──────────────────────────────────────────────────────────
# Dependencias compartidas entre dev y prod
FROM python:3.11-slim AS base

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage: dev ───────────────────────────────────────────────────────────
FROM base AS dev

# Copiar entrypoint y hacerlo ejecutable
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]


# ── Stage: prod ──────────────────────────────────────────────────────────
FROM base AS prod

# Copiar código de la aplicación
COPY . .

# Instalar servidor production-grade
RUN pip install --no-cache-dir gunicorn==21.2.0

EXPOSE 8000

CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
