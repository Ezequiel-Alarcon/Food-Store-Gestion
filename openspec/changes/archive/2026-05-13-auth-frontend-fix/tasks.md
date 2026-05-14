## 1. Tipos de respuesta

- [x] 1.1 Actualizar `LoginResponse` en `lib/api.ts` — cambiar `accessToken`/`refreshToken` a snake_case, eliminar campo `user`, agregar `PerfilResponse`

## 2. Auth Store

- [x] 2.1 Actualizar `authStore.ts` — desestructurar con snake_case, agregar fetch a `/perfil` para obtener `User` post-login/register, arreglar interceptor de refresh
