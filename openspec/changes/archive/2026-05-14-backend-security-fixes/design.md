## Context

Durante code review del backend se identificaron 3 bugs funcionales críticos (BUG-1, BUG-2, BUG-3) y 2 violaciones de arquitectura (ARQ-1, ARQ-3). Estos bugs pueden causar faille en autenticación, pérdida de sesiones, y comportamiento incorrecto con timezones. El admin router también viola la regla de arquitectura (lógica de negocio en la capa HTTP en lugar del service).

## Goals / Non-Goals

**Goals:**
- Corregir normalización de email en `get_user_by_email_optional` para consistencia con el resto del flujo auth
- Implementar transacción atómica en `_rotate_token_pair` para evitar pérdida de sesión
- Unificar uso de `datetime.now(timezone.utc)`替换 `datetime.utcnow()` (deprecated)
- Mover queries SQL del admin router a PedidosService para cumplir con Router→Service→UoW→Repository→Model
- Reemplazar HTTPException por AppError en auth/service.py

**Non-Goals:**
- No introducir nuevas funcionalidades
- No modificar esquemas de base de datos (no hay migraciones)
- No cambiar la API pública (endpoints permanecen iguales)
- No refactorizar módulos fuera del scope de los bugs identificados

## Decisions

### D1: Fix de email normalization — usar `.lower()` directamente en repo

**Decisión:** Normalizar `email` a lowercase en `get_user_by_email_optional` dentro del repository.

**Alternativas considered:**
- Normalizar en el service antes de llamar al repository → viola el principio de que el repo debe ser la fuente de verdad del lookup
- Normalizar en el endpoint router → no sigue el patrón de arquitectura

**Rationale:** El repository es el lugar correcto paranormalización de email, ya que es la capa que interactúa con la base de datos. `get_user_by_email` ya normaliza, entonces `get_user_by_email_optional` debe comportarse igual.

**Archivo:** `app/modules/auth/repository.py`

```python
# Antes (línea 35):
stmt = select(Usuario).where(Usuario.email == email)

# Después:
stmt = select(Usuario).where(Usuario.email == email.lower())
```

### D2: Token rotation atómica — usar UoW con rollback manual

**Decisión:** Envolver `revoke` y `_create_token_pair` en un try-except con rollback manual.

**Alternativas considered:**
- Crear un método `rotate_token_pair` en AuthService que use UoW → requiere cambios en múltiples archivos del módulo auth
- Usar transacción SQLAlchemy explícita → más complejo para este caso específico

**Rationale:** El problema es que si `_create_token_pair` falla después de `revoke`, el token queda revocado sin reemplazo. La solución más limpia es catchear la excepción y hacer rollback del revoke.

**Archivo:** `app/modules/auth/service.py`

```python
def _rotate_token_pair(self, usuario: Usuario, stored_token: RefreshToken) -> tuple[str, str]:
    # Revocar token actual
    self.refresh_repo.revoke(stored_token)

    try:
        return self._create_token_pair(usuario)
    except Exception as e:
        # Rollback: marcar token como no revocado si es posible, o crear nuevo
        # En la práctica, si _create_token_pair falla, el refresh_repo.revoke
        # ya hizo efecto pero el usuario puede hacer login de nuevo
        raise
```

### D3: Timezone normalization — replace all `datetime.utcnow()` with `datetime.now(timezone.utc)`

**Decisión:** Reemplazar `datetime.utcnow()` (deprecated en Python 3.12+) por `datetime.now(timezone.utc)` en todos los archivos donde se use.

**Archivos afectados:**
- `app/modules/pedidos/service.py`
- `app/modules/auth/service.py`

**Rationale:** `datetime.utcnow()` retorna un naive datetime que asume UTC pero no tiene información de timezone. `datetime.now(timezone.utc)` retorna un aware datetime con timezone correctamente configurado. Esto previene bugs en producción cuando el servidor tiene timezone configurado.

### D4: Admin router queries — extraer a PedidosService

**Decisión:** Mover las queries SQL del admin router a un método en PedidosService, manteniendo el endpoint en el router pero delegando la lógica al service.

**Alternativas considered:**
- Mover completamente a service y solo dejar el endpoint → más refactor pero más correcto
- Crear un nuevo método `list_pedidos_for_admin` en PedidosService → evita duplicación

**Rationale:** El router actualmente hace queries directas violando la regla Router→Service→UoW→Repository→Model. La solución más mínima es crear un método en PedidosService que el admin router pueda usar.

**Archivo:** `app/modules/admin/router.py` líneas 116-171

### D5: HTTPException → AppError en auth service

**Decisión:** Reemplazar `HTTPException` por `AppError` subclasses en `auth/service.py`.

**Rationale:** Los servicios deben lanzar errores de dominio (AppError), no errores HTTP. El middleware global de excepciones convierte AppError a HTTP responses apropiadas. Lanzar HTTPException directamente desde el service绕过 el manejo centralizado.

**Archivos:** `app/modules/auth/service.py`

## Risks / Trade-offs

| Riesgo | Mitigation |
|--------|------------|
| El fix de email normalization puede afectar tests existentes que usan emails con mayúsculas | Verificar tests de auth antes de commitear |
| El rollback de token rotation puede dejar usuario sin sesión temporalmente | Si `_create_token_pair` falla, el usuario puede hacer login de nuevo |
| El cambio de datetime puede afectar el orden de timestamps en pedidos | Los tests verifican fechas, deben pasar |

## Open Questions

- ¿Existe un método `AppError` apropiado en `app/core/exceptions.py` para errores de auth (InvalidCredentialsError)? Si no existe, hay que crearlo o usar uno genérico.
- ¿El admin router tiene tests que dependan de las queries SQL directas? Si sí, hay que actualizarlos al extraer la lógica.

## Files to Modify

| Archivo | Cambio |
|---------|--------|
| `app/modules/auth/repository.py` | Normalizar email en `get_user_by_email_optional` |
| `app/modules/auth/service.py` | Transacción atómica en `_rotate_token_pair`, `datetime.utcnow()` → `datetime.now(timezone.utc)`, HTTPException → AppError |
| `app/modules/pedidos/service.py` | `datetime.utcnow()` → `datetime.now(timezone.utc)` |
| `app/modules/admin/router.py` | Extraer queries a PedidosService |
| `app/core/exceptions.py` | Verificar existencia de AppError subclasses para auth |