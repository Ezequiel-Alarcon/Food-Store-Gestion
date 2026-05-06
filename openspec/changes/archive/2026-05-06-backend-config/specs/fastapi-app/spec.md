## ADDED Requirements

### Requirement: FastAPI app con CORS configurado
La aplicación FastAPI debe permitir请求 desde orígenes configurables mediante CORS middleware.

#### Scenario: CORS permitido para origen válido
- **WHEN** frontend envía request desde http://localhost:5173
- **THEN** respuesta incluye headers Access-Control-Allow-Origin correctos

#### Scenario: CORS bloqueado para origen inválido
- **WHEN** frontend envía request desde http://malicious.com
- **THEN** respuesta bloqueada por CORS policy

### Requirement: Rate limiting en endpoint de login
El endpoint POST /api/v1/auth/login debe tener rate limiting de 5 intentos por IP cada 15 minutos.

#### Scenario: Rate limit alcanzado
- **WHEN** usuario realiza más de 5 intentos fallidos de login en 15 minutos
- **THEN** servidor responde HTTP 429 con header Retry-After

#### Scenario: Rate limit no alcanzado
- **WHEN** usuario realiza hasta 5 intentos de login
- **THEN** servidor procesa cada request normalmente

### Requirement: Exception handlers RFC 7807
Todos los errores HTTP deben seguir el formato Problem Details (RFC 7807).

#### Scenario: Error de validación
- **WHEN** cliente envía datos inválidos
- **THEN** respuesta es JSON con estructura {"detail": "...", "type": "...", "status": N}

#### Scenario: Error interno
- **WHEN** servidor lanza excepción no manejada
- **THEN** respuesta es JSON con estructura RFC 7807 y código 500