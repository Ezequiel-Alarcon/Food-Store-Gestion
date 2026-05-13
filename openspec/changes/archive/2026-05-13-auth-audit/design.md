## Context

El módulo `auth` fue implementado como parte del change `auth-backend` (#6). Sin embargo, la implementación tiene 22 bugs identificados, desde el Swagger mostrando un formulario OAuth2 inexistente hasta el seed de datos completamente roto. Adicionalmente, hay discrepancias entre los specs OPSX, la documentación `docs/Integrador.txt` v5.0 (source of truth), y el código real.

El change `auth-audit` es un saneamiento integral — no agrega features nuevas, corrige bugs y alinea implementación con documentación.

**Principio rector:** `docs/Integrador.txt` v5.0 + `docs/Historias_de_usuario.txt` (reglas de negocio RN-AU*) son el source of truth. Donde specs OPSX y código difieran, ganan los docs.

## Goals / Non-Goals

**Goals:**
- Swagger `/docs` muestre un campo simple para Bearer token, sin formulario OAuth2
- Seed data funcione con modelos reales (crea roles + admin)
- `RolEnum` contenga los 4 roles del spec (ADMIN, STOCK, PEDIDOS, CLIENT)
- Login no filtre info de cuenta (RN-AU08: mismo mensaje para email inexistente, password mal, usuario inactivo)
- Usuarios desactivados no puedan refreshear tokens
- Rate limiting funcione (agregar `SlowAPIMiddleware`)
- Validación de password complejo (1 mayúscula, 1 número)
- `RegisterRequest` incluya `apellido` (requerido por docs)
- Consistencia de datetime (aware en todo el módulo)
- `response_model` explícito en todos los endpoints de auth

**Non-Goals:**
- Implementar modelo M:N `UsuarioRol` con tabla pivote (cambio arquitectónico grande → change separado)
- Cambiar `created_at`/`updated_at` a `creado_en`/`actualizado_en` (requiere migración de columnas → riesgo de breaking)
- Agregar `password_confirmation` al `RegisterRequest` (validación frontend → responsabilidad del cliente)
- Refactorizar servicios para usar UoW (BUG #13 → change separado de arquitectura)
- Implementar `GET /api/v1/auth/me` (endpoint listado en docs pero no implementado → change separado)

## Decisions

### D1: Swagger auth → `HTTPBearer` (no `OAuth2PasswordBearer`)

**Decisión:** Reemplazar `OAuth2PasswordBearer(tokenUrl="token")` por `HTTPBearer()` en `app/core/deps.py`.

**Alternativas consideradas:**
- `OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")` — Corrige la URL pero sigue mostrando formulario OAuth2 con `client_id`/`client_secret` que no existen. Swagger haría POST con `username` (no `email`) y `grant_type=password` — incompatible con nuestro endpoint.
- `OpenAPI custom security scheme` — Overkill, `HTTPBearer` resuelve el problema con 1 línea.
- `APIKeyHeader` — Menos semántico, no es estándar para JWT.

**Rationale:** La app usa JWT Bearer tokens simples. `HTTPBearer` extrae el token del header `Authorization: Bearer <token>` igual que `OAuth2PasswordBearer`, pero Swagger muestra solo un campo **Value** para pegar el token — sin formulario OAuth2.

### D2: RolEnum → 4 roles (reemplazar GESTOR por STOCK + PEDIDOS)

**Decisión:** `RolEnum` pasa de `{ADMIN, GESTOR, CLIENT}` a `{ADMIN, STOCK, PEDIDOS, CLIENT}`.

**Rationale:** `docs/Integrador.txt` v5.0 y `docs/Historias_de_usuario.txt` (RN-RB01-RB10) definen 4 roles con nombres específicos. `GESTOR` era un placeholder genérico que no distinguía stock de pedidos. El AGENTS.md dice explícitamente: "4 roles: Cliente, Admin, Gestor de Stock, Gestor de Pedidos".

**Impacto en routers existentes:** Verificar y actualizar dependencias `require_role("GESTOR")` → `require_role("STOCK", "PEDIDOS")` o el rol específico según el endpoint.

### D3: Seed → usar modelos reales (sin Rol ni UsuarioRol)

**Decisión:** El seed usa directamente `Usuario` con `rol: str` para asignar roles, sin necesidad de tablas `Rol`/`UsuarioRol` que no existen.

**Rationale:** Los modelos `Rol` y `UsuarioRol` están en el ERD v5.0 de los docs pero NO implementados. Implementarlos requeriría migraciones, nuevas tablas, y refactorización del RBAC. Demasiado scope para este change de bugfixing. El seed funciona con el modelo actual (flat `rol` string).

**Cambio en seed.py:**
- Eliminar imports condicionales de `Rol`, `UsuarioRol` (no existen)
- `seed_roles()` → comentado (no hay tabla Rol), o adaptado para loguear los 4 roles sin insertar
- `seed_usuario_admin()` → usar campos reales del modelo: `nombre`, `email`, `password_hash`, `rol="ADMIN"`, `telefono`, `activo=True`, `created_at`, `updated_at`

### D4: Token type `"access"` en JWT payload

**Decisión:** Agregar `"type": "access"` al payload del access token generado por `create_access_token()` en `app/core/security.py`.

**Rationale:** `get_current_user()` en `deps.py` línea 62-68 chequea `token_type = payload.get("type")`. Si bien actualmente funciona porque `None != "access"` es `False`, es frágil. Si alguien envía un refresh token como access token, debería fallar explícitamente. Agregar `type: "access"` cierra el gap.

### D5: Login → mensaje genérico para todos los casos de fallo (RN-AU08)

**Decisión:** Unificar los 3 casos de fallo de login bajo un mismo mensaje: `"Credenciales inválidas"`.

**Casos actuales:**
| Condición | Mensaje actual | Mensaje corregido |
|---|---|---|
| Email no existe | "Credenciales inválidas" | "Credenciales inválidas" ✅ |
| Password incorrecto | "Credenciales inválidas" | "Credenciales inválidas" ✅ |
| Usuario inactivo | "Usuario desactivado" ❌ | "Credenciales inválidas" |

**Rationale:** RN-AU08: "Login NO diferencia 'email no existe' de 'contraseña incorrecta'". Extender esto a usuario inactivo previene enumeración de cuentas.

### D6: Datetime → `datetime.now(timezone.utc)` en todo el módulo

**Decisión:** Reemplazar `datetime.utcnow()` (naive) por `datetime.now(timezone.utc)` (aware) en modelos y repositorios. La migración de columnas de `DateTime` a `DateTime(timezone=True)` requiere una nueva migración Alembic.

**Rationale:** `datetime.utcnow()` produce datetimes naive que PostgreSQL no puede comparar correctamente con valores aware. Esto rompe el chequeo de expiración de refresh tokens (`expires_at > datetime.utcnow()`).

### D7: Rate limiting → agregar `SlowAPIMiddleware`

**Decisión:** Agregar `app.add_middleware(SlowAPIMiddleware)` en `main.py`, ANTES de los demás middlewares.

**Rationale:** Sin el middleware, `slowapi` no trackea requests y `@limiter.limit()` es un no-op. Es la razón por la que el rate limiting probablemente nunca funcionó (BUG #20).

## Risks / Trade-offs

- **[Riesgo] Romper endpoints existentes que usan `GESTOR`** → Mitigación: grep completo de `require_role.*GESTOR` antes de cambiar, actualizar todos los usos.
- **[Riesgo] Migración de columnas datetime puede fallar con datos existentes** → Mitigación: migración con `ALTER COLUMN ... TYPE TIMESTAMPTZ USING columna AT TIME ZONE 'UTC'`.
- **[Riesgo] `RegisterRequest.apellido` es breaking para clientes** → Mitigación: documento en el changelog. Los clientes que no envíen `apellido` recibirán 422. En desarrollo esto no es problema.
- **[Trade-off] No implementar `UsuarioRol` ahora** → El RBAC sigue siendo flat (un rol por usuario). Aceptable para el scope de bugfixing. La tabla M:N se implementará en un change futuro.
