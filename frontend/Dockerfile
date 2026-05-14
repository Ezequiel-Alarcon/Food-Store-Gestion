# ── Stage: base ──────────────────────────────────────────────────────────
# Dependencias compartidas entre dev y prod
FROM node:18-alpine AS base

WORKDIR /app

# Copiar package files y instalar dependencias
COPY package*.json ./
RUN npm ci

# ── Stage: dev ───────────────────────────────────────────────────────────
FROM base AS dev

EXPOSE 5173

CMD ["sh", "-c", "echo '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n  Food Store Frontend — React + Vite\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n  Local: http://localhost:5173\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n' && npm run dev -- --host 0.0.0.0"]


# ── Stage: build (PROD — activar cuando se necesite build productivo) ────
# FROM base AS build
# COPY . .
# RUN npm run build
#
# ── Stage: prod (PROD — activar junto con build) ─────────────────────────
# FROM nginx:alpine AS prod
# COPY --from=build /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
