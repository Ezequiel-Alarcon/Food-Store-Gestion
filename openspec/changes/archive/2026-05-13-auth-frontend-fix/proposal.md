## Why

El backend `auth-audit` cambió el `TokenResponse` eliminando el campo `user` y usando snake_case (`access_token`, `refresh_token`). El frontend (`auth-frontend`) no se actualizó, quedando con tipos camelCase (`accessToken`, `refreshToken`) y esperando un campo `user` inexistente. Esto rompe el flujo de autenticación: el token se guarda como `undefined` y el usuario autenticado no tiene datos de perfil visibles.

## What Changes

- Corregir `LoginResponse` en `lib/api.ts` para usar snake_case (`access_token`, `refresh_token`)
- Actualizar `authStore.ts` para desestructurar correctamente y obtener datos del usuario vía `/perfil` post-login/register

## Capabilities

### Modified Capabilities
- `user-login`: La respuesta de login/register ahora requiere llamada adicional a `/perfil` para obtener datos del usuario
- `user-registration`: Ídem

## Impact

- `frontend/src/lib/api.ts`: tipos de respuesta de auth
- `frontend/src/stores/authStore.ts`: lógica de login/register
