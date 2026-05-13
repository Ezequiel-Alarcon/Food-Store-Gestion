## ADDED Requirements

### Requirement: SlowAPIMiddleware must be added to FastAPI app
El sistema SHALL agregar `SlowAPIMiddleware` a la aplicación FastAPI mediante `app.add_middleware(SlowAPIMiddleware)` en `main.py`. Sin este middleware, las directivas `@limiter.limit()` no tienen efecto y el rate limiting no funciona.

#### Scenario: Middleware is registered before other middlewares
- **WHEN** la aplicación FastAPI inicia
- **THEN** SlowAPIMiddleware está registrado y procesa requests

#### Scenario: Rate limit decorator is enforced
- **WHEN** un endpoint tiene el decorador `@limiter.limit("5/minute")`
- **THEN** el middleware slowapi trackea los requests por IP y aplica el límite configurado
