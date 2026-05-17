## Context

El módulo `perfil` del backend está implementado desde la Fase 1 (change `auth-backend`). Expone 3 endpoints bajo `/api/v1/perfil`:

| Método | Path | Body | Response |
|--------|------|------|----------|
| `GET` | `/perfil` | — | `{ id, email, nombre, apellido, rol, telefono, activo, created_at }` |
| `PUT` | `/perfil` | `{ nombre?, apellido?, telefono? }` | Misma estructura que GET |
| `PUT` | `/perfil/password` | `{ current_password, new_password }` | `{ message }` |

El frontend solo consume `GET /perfil` internamente en `authStore.ts` para poblar los datos del usuario tras login/register. No hay página, ruta, ni queries de TanStack Query para que el usuario interactúe con su perfil.

## Goals / Non-Goals

**Goals:**
- Permitir al usuario autenticado ver sus datos personales (nombre, apellido, email, teléfono, rol)
- Permitir editar nombre, apellido y teléfono con feedback inmediato
- Permitir cambiar contraseña con validación client-side + server-side
- Actualizar el `authStore.user` al editar el perfil para reflejar cambios en la UI global
- Seguir las convenciones FSD: entidad en `entities/perfil/`, página en `pages/ProfilePage.tsx`

**Non-Goals:**
- No se modifica el backend
- No se crea `features/perfil/` porque no hay componentes reutilizables (es una sola página autónoma)
- No se agrega cambio de email (requiere flujo de verificación que está fuera de scope)
- No se agrega subida de avatar/foto de perfil

## Decisions

### 1. Entidad en `entities/perfil/`, página en `pages/ProfilePage.tsx`

**Elegido:** Seguir el patrón FSD con la entidad en `entities/` y la página en `pages/`.

**Alternativa considerada:** `features/perfil/`. Se descartó porque la ProfilePage es una sola vista sin componentes reutilizables, similar a `CatalogPage.tsx` o `CartPage.tsx` que también viven en `pages/`. `features/` se reserva para features con múltiples subcomponentes (auth, cart, admin, addresses).

### 2. Estado del servidor con TanStack Query

**Elegido:** `useQuery` para GET perfil (con `staleTime` alto, los datos de perfil no cambian frecuentemente) y `useMutation` para PUT perfil y PUT password. Al mutar perfil, se invalida la query y se actualiza `authStore.user`.

**Alternativa considerada:** Manejar estado local con `useState` + `useEffect`. Se descartó porque rompe la convención del proyecto: "Estado del servidor exclusivamente con TanStack Query".

### 3. Formulario unificado en una sola página con dos secciones

**Elegido:** Una página `ProfilePage.tsx` con dos cards/secciones: "Datos personales" (lectura/edición) y "Cambiar contraseña" (formulario independiente).

**Alternativa considerada:** Dos páginas separadas (`/perfil` y `/perfil/password`). Se descartó por simplicidad — son 3 campos editables + 2 campos de password, no justifica navegación extra.

### 4. No se usa `@tanstack/react-form`

**Elegido:** Formularios con estado local `useState` + `onSubmit`, mismo patrón que `MisDireccionesPage.tsx`.

**Alternativa considerada:** TanStack Form. Se descartó porque ningún formulario del proyecto lo usa actualmente. Consistencia con el código existente.

## Risks / Trade-offs

- **[Bajo] Inconsistencia de datos entre `authStore.user` y backend:** Si otro admin modifica el usuario mientras el cliente tiene la página abierta, los datos mostrados pueden desfasarse. → Mitigación: `staleTime: 0` en `useQuery` para GET perfil (siempre fresco), y `refetchOnWindowFocus: true`.
- **[Bajo] Logout forzado al cambiar contraseña:** El backend invalida todos los refresh tokens al cambiar la contraseña (RN-AU05). El frontend debe manejar esto: si el token viejo falla, el interceptor de `api.ts` ya hace refresh → logout → redirect a `/login`.
