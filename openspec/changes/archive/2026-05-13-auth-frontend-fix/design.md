## Context

El backend devuelve `TokenResponse` con `access_token`, `refresh_token`, `token_type`, `expires_in`. El frontend definía `LoginResponse` con `accessToken`, `refreshToken`, `user`. Hay un mismatch snake_case ↔ camelCase y falta el campo `user` en la respuesta real.

## Decisiones

### D1: Usar snake_case en los tipos del frontend

Cambiar `LoginResponse.accessToken` → `access_token` y `refreshToken` → `refresh_token`. Es un cambio mínimo que alinea el frontend con la realidad del backend sin requerir transformers ni cambios en el backend.

### D2: Obtener `user` vía endpoint `/perfil` después del login/register

Como el backend ya no incluye `user` en `TokenResponse`, el frontend debe llamar a `GET /api/v1/perfil` después de obtener los tokens. Esto devuelve `{nombre, apellido, email, rol}` que se mapea al `User` del store.
