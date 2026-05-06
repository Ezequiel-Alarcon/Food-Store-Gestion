# auth-store

Zustand store para gestión de autenticación.

## Estado Inicial

```typescript
interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: {
    id: number;
    nombre: string;
    email: string;
    roles: string[];
  } | null;
  isAuthenticated: boolean;
}
```

## Acciones Requeridas

- `login(tokens, user)`: Set accessToken, refreshToken, user, isAuthenticated=true
- `logout()`: Clear todo, set isAuthenticated=false
- `updateTokens(tokens)`: Solo actualizar tokens (sin cambiar user)
- `setUser(user)`: Actualizar datos del usuario

## Selectores Requeridos

- `isAuthenticated()`: Retorna boolean
- `hasRole(role: string)`: Retorna boolean - verifica si el usuario tiene el rol

## Persistencia

**Middleware:** Zustand persist
**Storage key:** `food-store-auth`
**Partialize:** Solo `accessToken` se persiste

> **Importante:** El refreshToken NO se persiste por seguridad. Se guarda en memoria y se usa solo para el interceptor.

## Criterios de Éxito

- [ ] login() setea todos los campos correctamente
- [ ] logout() limpia todo
- [ ] isAuthenticated() retorna false al inicio
- [ ] hasRole() funciona correctamente
- [ ] Access token persiste en localStorage
- [ ] Recargar la página reconstructiona el estado desde localStorage