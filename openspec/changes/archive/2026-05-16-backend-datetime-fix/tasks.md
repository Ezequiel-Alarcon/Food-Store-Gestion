## 1. Migrar productos/service.py

- [x] 1.1 Reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en líneas 353 y 409 (`actualizado_en`)
- [x] 1.2 Verificar que `timezone` esté importado desde `datetime`

## 2. Migrar productos/repository.py

- [x] 2.1 Reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en líneas 182, 194, 209, 225, 227, 245 (`actualizado_en`, `eliminado_en`)
- [x] 2.2 Verificar que `timezone` esté importado desde `datetime`

## 3. Migrar sucursales/service.py

- [x] 3.1 Reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en líneas 30, 31 (`created_at`, `updated_at`) y 45 (`updated_at`)
- [x] 3.2 Verificar que `timezone` esté importado desde `datetime`

## 4. Migrar direcciones/service.py

- [x] 4.1 Reemplazar `datetime.utcnow()` → `datetime.now(timezone.utc)` en líneas 68, 69, 103, 120, 141, 168, 182, 183, 209, 222 (`created_at`, `updated_at`)
- [x] 4.2 Verificar que `timezone` esté importado desde `datetime`

## 5. Verificación

- [x] 5.1 Ejecutar `grep -r "utcnow" backend/app/modules/` — debe retornar 0 resultados
- [x] 5.2 Commit con mensaje: `fix: replace datetime.utcnow() with datetime.now(timezone.utc)`