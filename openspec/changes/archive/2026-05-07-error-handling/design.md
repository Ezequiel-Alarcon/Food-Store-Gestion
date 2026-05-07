## Context

El backend actual no tiene un manejo de errores estandarizado. Cada endpoint puede devolver respuestas de error en formatos diferentes (string plano, JSON improvisado, HTTPException default de FastAPI), lo que dificulta al frontend parsear errores consistentemente. Además, no hay rate limiting ni validación centralizada de inputs.

Este change introduce un manejo de errores RFC 7807, validación de inputs en Pydantic schemas, y rate limiting con slowapi.

## Goals / Non-Goals

**Goals:**
- Estandarizar todas las respuestas de error del API bajo RFC 7807 (Problem Details).
- Centralizar validación de inputs en schemas Pydantic (Create/Update) para todos los módulos.
- Implementar rate limiting por IP (endpoints públicos) y por usuario autenticado (endpoints sensibles).
- Proveer excepciones custom que mapparen errores de dominio a códigos HTTP específicos.

**Non-Goals:**
- Implementar logging centralizado (eso viene en un change futuro de observabilidad).
- Validación de reglas de negocio (eso se hace en los services, no en schemas).
- Rate limiting por servicio o por recurso específico (solo IP y user).

## Decisions

1) **RFC 7807 como formato de error**
- **Decisión**: Usar el formato RFC 7807 para todas las respuestas de error del API, incluyendo `type`, `title`, `status`, `detail`, `instance`.
- **Rationale**: Estándar IETF adoptado por FastAPI/Pydantic. El frontend puede parsear consistentemente errores y mostrar mensajes apropiados.
- **Alternativas**:
  - Formato custom por módulo: genera inconsistencia y trabajo duplicado.
  - Solo HTTPException default: poco informativo para el cliente.

2) **Excepciones custom en `core/exceptions.py`**
- **Decisión**: Crear clases de excepción que extienden de `Exception` y que el middleware convierte a formato RFC 7807. Ejemplos: `NotFoundError`, `ValidationError`, `UnauthorizedError`, `ForbiddenError`, `RateLimitError`.
- **Rationale**: Permite lanzar errores semánticos desde los services y guarantee formato uniforme en la respuesta.
- **Alternativas**:
  - Usar solo HTTPException de FastAPI: menos flexible para mapeo de errores de dominio.

3) **Middleware de error handler global**
- **Decisión**: Crear `ErrorHandlerMiddleware` en `core/middleware.py` que capture todas las excepciones y las convierta a `ProblemDetail` response.
- **Rationale**: Centraliza el manejo en un solo lugar, evita try/except repetidos en cada router, y guarantee que ninguna excepción escape sin formato.
- **Alternativas**:
  - Try/except por endpoint: propenso a olvidar casos y duplicación.

4) **Validación en schemas Pydantic (Create/Update)**
- **Decisión**: Usar `Field()` de Pydantic con validators para sanitizar strings (strip, lower, etc.) y validar formatos (email, phone, etc.).
- **Rationale**: La validación de inputs es la primera línea de defensa. Centralizarla en schemas DRY y mantenible.
- **Alternativas**:
  - Validación manual en services: propenso a errores y duplicación.

5) **Rate limiting con slowapi**
- **Decisión**: Usar slowapi con límites por defecto: 60 req/min por IP para endpoints públicos, 100 req/min por usuario autenticado para endpoints sensibles.
- **Rationale**: Simple de implementar, almacenamiento en memoria (OK para single instance), extensible a Redis para multi-instance.
- **Alternativas**:
  - Custom middleware con Redis: overkill para el scope inicial.
  - No rate limiting: exposición a ataques de fuerza bruta.

## Risks / Trade-offs

- **[Riesgo]** Rate limiting en memoria no escala horizontalmente → **Mitigación**: Diseñar para poder migrar a Redis store sin cambiar la API de rate limiting.
- **[Riesgo]** El middleware de error puede ocultar errores de desarrollo → **Mitigación**: En desarrollo (`DEBUG=true`) devolver stack trace completo en `detail`.
- **[Trade-off]** Validación estricta en schemas puede romper BC con clientes existentes → **Mitigación**: Validación solo en endpoints nuevos; los existentes se migran gradualmente.

## Open Questions

- ¿Se necesita un endpoint de health check excluido del rate limiting?
- ¿El rate limit para endpoints de auth (login) debe ser más estricto (5 req/min)?