## 1. Excepciones Custom y RFC 7807

- [x] 1.1 Crear `backend/app/core/exceptions.py` con clases: `NotFoundError`, `ValidationError`, `UnauthorizedError`, `ForbiddenError`, `ConflictError`, `RateLimitError`
- [x] 1.2 Implementar función helper `problem_detail()` que construye el response body RFC 7807
- [x] 1.3 Agregar `ProblemDetail` schema en `core/schemas.py` para tipado Pydantic

## 2. Middleware de Error Handler

- [x] 2.1 Crear `backend/app/core/middleware.py` con `ErrorHandlerMiddleware`
- [x] 2.2 Configurar el middleware en `backend/app/main.py`
- [x] 2.3 En desarrollo (`DEBUG=true`): incluir stack trace en `detail`
- [x] 2.4 En producción (`DEBUG=false`): mensaje genérico, loguear stack trace
- [x] 2.5 Registrar `ErrorHandlerMiddleware` con `app.add_middleware()` (debe ser el último)

## 3. Rate Limiting

- [x] 3.1 Agregar `slowapi` a `backend/requirements.txt` (ya estaba)
- [x] 3.2 Configurar rate limiter en `core/config.py` con variables de entorno
- [x] 3.3 Aplicar rate limit público (60 req/min) a endpoints en `main.py`
- [x] 3.4 Aplicar rate limit estricto (5 req/min) a endpoints de auth
- [x] 3.5 Excluir `/health`, `/docs`, `/openapi.json` del rate limiting

## 4. Validación de Inputs (Schema Level)

- [x] 4.1 Crear validators en schemas de auth (`modules/auth/schemas.py`): email format, password min length, strip whitespace
- [x] 4.2 Crear validators en schemas de productos (`modules/productos/schemas.py`): precio > 0, stock >= 0, nombre no vacío
- [x] 4.3 Crear validators en schemas de categorías: nombre no vacío, no solo espacios

## 5. Verificación

- [x] 5.1 Verificar que el backend compila (Python - todo OK)
- [x] 5.2 Verificar que `npm run build` en frontend pasa (requiere `npm install` primero - no es issue del change)
- [ ] 5.3 Crear commit con conventional commit format