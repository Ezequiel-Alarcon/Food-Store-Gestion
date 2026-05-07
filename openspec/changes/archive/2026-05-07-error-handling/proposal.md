## Why

El backend actual carece de un manejo de errores estructurado y consistente. Los errores son capturados de forma ad-hoc, devolviendo respuestas inconsistentes que dificultan al frontend parsear y mostrar mensajes adecuados. Sin un estándar como RFC 7807, cada endpoint puede devolver un formato diferente, y sin rate limiting ni validación centralizada, el sistema está expuesto a ataques de fuerza bruta y inputs maliciosos.

## What Changes

- Se introduce **RFC 7807 (Problem Details)** para todas las respuestas de error del API, con formato consistente: `type`, `title`, `status`, `detail`, `instance`.
- Se crean **excepciones custom** en `backend/app/core/exceptions.py` que mapean errores de dominio a códigos HTTP y formato RFC 7807.
- Se implementa un **middleware de error handler** que captura todas las excepciones no manejadas y las convierte en respuestas estructuradas.
- Se agrega **validación de inputs** centralizada con Pydantic en los schemas de request para sanitizar y validar antes de llegar a los services.
- Se configura **rate limiting** por IP y por usuario autenticado usando slowapi para prevenir ataques de fuerza bruta.

## Capabilities

### New Capabilities
- `rfc-7807-errors`: Manejo de errores estandarizado RFC 7807 para todos los endpoints del API.
- `input-validation`: Validación y sanitización de inputs en schemas Pydantic (Create/Update).
- `rate-limiting`: Rate limiting configurable por endpoint y por usuario.

### Modified Capabilities
- (none)

## Impact

- Backend: `backend/app/core/exceptions.py` (nuevo), `backend/app/core/middleware.py` (nuevo), schemas de todos los módulos con validación Pydantic.
- Afecta cómo el frontend consume errores del API — requiere ajustar el interceptor para manejar el formato RFC 7807.
- Dependencias nuevas: `pydantic` (ya incluido con FastAPI), `slowapi` para rate limiting.